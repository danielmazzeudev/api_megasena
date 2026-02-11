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
                    last_saved = max(item['draw_number'] for item in complete_history)
                    start_draw = last_saved + 1
                    print(f"Existing file found. Last draw: {last_saved}. Starting from: {start_draw}")
        except Exception as e:
            print(f"Error reading existing file: {e}")

    try:
        latest_response = requests.get(base_url, timeout=15)
        if latest_response.status_code == 200:
            data_list = latest_response.json()
            latest_draw = data_list[0].get("concurso") if isinstance(data_list, list) else data_list.get("concurso")
            end_draw = latest_draw
        else:
            print("Could not determine latest draw.")
            return
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return

    if start_draw > end_draw:
        print("Your history is already up to date.")
        return

    print(f"Updating from {start_draw} to {end_draw}")
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
                    "winners_4_numbers": awards[2].get("ganhadores") if len(awards) > 2 else 0,
                    "winners_5_numbers": awards[1].get("ganhadores") if len(awards) > 1 else 0,
                    "winners_6_numbers": awards[0].get("ganhadores") if len(awards) > 0 else 0,
                    "prize_value_4_numbers": awards[2].get("valorPremio") if len(awards) > 2 else 0,
                    "prize_value_5_numbers": awards[1].get("valorPremio") if len(awards) > 1 else 0,
                    "prize_value_6_numbers": awards[0].get("valorPremio") if len(awards) > 0 else 0,
                    "accumulated_prize_value": data.get("valorAcumuladoProximoConcurso", 0.0)
                }
                
                complete_history.append(item)
                
                with open(output_filename, 'w', encoding='utf-8') as f:
                    json.dump(complete_history, f, ensure_ascii=False, indent=4)
                
                print(f"Draw [{item['draw_number']}] saved.")

            elif response.status_code == 429:
                print("Rate limit reached. Waiting 30 seconds...")
                time.sleep(30)
            
            time.sleep(0.15)

        except Exception as e:
            print(f"Failure in draw {draw_number}: {e}")
            continue

    print("-" * 75)
    print(f"Update complete! Total records: {len(complete_history)}")

if __name__ == "__main__":
    fetch_mega_sena_history()