import requests
import json
import time
import os

def fetch_mega_sena_history():
    output_filename = 'megasena.json'
    complete_history = []
    start_draw = 1
    base_url = "https://loteriascaixa-api.herokuapp.com/api/megasena/"

    if os.path.exists(output_filename):
        try:
            with open(output_filename, 'r', encoding='utf-8') as f:
                complete_history = json.load(f)
                if complete_history:
                    last_saved = max(item.get('draw_number', 0) for item in complete_history)
                    start_draw = last_saved + 1
                    print(f"Arquivo encontrado. Último sorteio: {last_saved}. Retomando de: {start_draw}")
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")

    try:
        latest_response = requests.get(base_url, timeout=15)
        if latest_response.status_code == 200:
            data_list = latest_response.json()
            end_draw = data_list[0].get("concurso")
        else:
            print("Não foi possível determinar o último sorteio.")
            return
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return

    if start_draw > end_draw:
        print("Seu histórico já está atualizado.")
        return

    print(f"Atualizando de {start_draw} até {end_draw}")
    print(f"{'CONCURSO':<10} | {'DATA':<12} | {'DEZENAS':<20} | {'GANHADORES (6)'}")
    print("-" * 75)

    for draw_number in range(start_draw, end_draw + 1):
        try:
            response = requests.get(f"{base_url}{draw_number}", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                awards = data.get("premiacoes", [])
            
                item = {
                    "draw_number": data.get("concurso"),
                    "draw_date": data.get("data"),
                    "numbers": data.get("dezenas"),
                    "winners_6_numbers": awards[0].get("ganhadores") if len(awards) > 0 else 0,
                    "is_accumulated": data.get("acumulou", False),
                }
                
                complete_history.append(item)
                
                with open(output_filename, 'w', encoding='utf-8') as f:
                    json.dump(complete_history, f, ensure_ascii=False, indent=4)
                
                numbers_str = "-".join(item['numbers'])
                winners = item['winners_6_numbers']
                status = f"{winners} ganhador(es)" if winners > 0 else "ACUMULOU"
                
                print(f"{item['draw_number']:<10} | {item['draw_date']:<12} | {numbers_str:<20} | {status}")

            elif response.status_code == 429:
                print("\nLimite de requisições atingido. Aguardando 30 segundos...")
                time.sleep(30)
            
            time.sleep(0.1)

        except Exception as e:
            print(f"\nFalha no sorteio {draw_number}: {e}")
            continue

    print("-" * 75)
    print(f"Atualização concluída! Total de registros: {len(complete_history)}")

if __name__ == "__main__":
    fetch_mega_sena_history()