import requests
import json
import time
import os

def fetch_mega_sena_history():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = os.path.join(script_dir, 'megasena.json')
    
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
                    print(f"Arquivo existente. Ultimo sorteio: {last_saved}. Começando do: {start_draw}")
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")

    try:
        latest_response = requests.get(base_url, timeout=15)
        if latest_response.status_code == 200:
            data_list = latest_response.json()
            latest_draw = data_list[0].get("concurso")
            end_draw = latest_draw
        else:
            print("Não foi possível obter o último sorteio.")
            return
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return

    if start_draw > end_draw:
        print("Histórico já está atualizado.")
        return

    print(f"Atualizando do sorteio {start_draw} até {end_draw}")

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
                    "winners_4_numbers": awards[2].get("ganhadores") if len(awards) > 2 else 0,
                    "winners_5_numbers": awards[1].get("ganhadores") if len(awards) > 1 else 0,
                    "winners_6_numbers": awards[0].get("ganhadores") if len(awards) > 0 else 0,
                    "prize_value_4_numbers": awards[2].get("valorPremio") if len(awards) > 2 else 0,
                    "prize_value_5_numbers": awards[1].get("valorPremio") if len(awards) > 1 else 0,
                    "prize_value_6_numbers": awards[0].get("valorPremio") if len(awards) > 0 else 0,
                    "is_accumulated": data.get("acumulou", False),
                    "accumulated_prize": data.get("valorAcumuladoProximoConcurso", 0.0),
                    "estimated_next_prize": data.get("valorEstimadoProximoConcurso", 0.0)
                }
                complete_history.append(item)
                with open(output_filename, 'w', encoding='utf-8') as f:
                    json.dump(complete_history, f, ensure_ascii=False, indent=4)
                print(f"Sorteio [{item['draw_number']}] salvo.")
            time.sleep(0.1)
        except Exception as e:
            print(f"Falha no sorteio {draw_number}: {e}")
            continue

if __name__ == "__main__":
    fetch_mega_sena_history()