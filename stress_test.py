import requests

# Konfiguracja
URL = "http://192.168.0.83:5000/tasks/process-url?url=https://img.freepik.com/free-photo/people-posing-together-registration-day_23-2149096793.jpg?semt=ais_hybrid&w=740&q=80"
TOTAL_REQUESTS = 1000
TIMEOUT = 30.0

print(f"Rozpoczynam wysyłanie {TOTAL_REQUESTS} zapytań...")

success_count = 0
error_count = 0

for i in range(TOTAL_REQUESTS):
    try:
        response = requests.get(URL, timeout=TIMEOUT)

        # 200 (OK)
        # 202 (przyjęto do kolejki)
        if response.status_code in [200, 202]:
            print(f"[{i + 1}/{TOTAL_REQUESTS}] Sukces: {response.status_code} (Zadanie przyjęte)")
            success_count += 1
        else:
            print(f"[{i + 1}/{TOTAL_REQUESTS}] Błąd: {response.status_code}")
            error_count += 1

    except requests.exceptions.RequestException as e:
        print(f"[{i + 1}/{TOTAL_REQUESTS}] Wyjątek połączenia: {e}")
        error_count += 1

print("-" * 50)
print(f"Zakończono. Sukcesy: {success_count}, Błędy: {error_count}")
