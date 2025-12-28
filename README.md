# UEKAT_Advanced
Prosty system do zliczania osób na zdjęciach wykorzystujący:
- **Flask**
- **RabbitMQ**
- **OpenCV (YOLO)**
- **sqllite3**
- **docker-compose**

Aplikacja przetwarza zadania asynchronicznie przy użyciu workerów.

Wymagany jest zainstalowany Docker Compose.

#### Instrukcja uruchomienia:
```bash
   docker compose up --build
```
Wymagane pakiety znajdują się w requirments.txt oraz instalują się automatycznie (zdefiniowane w Dockerfile)

#### Endpointy
- GET	localhost:5000/tasks	Lista wszystkich zadań (wyniki analizy).
- GET	localhost:5000/tasks/<id>	Szczegóły konkretnego zadania.
- POST	localhost:5000/tasks/upload	Przesłanie pliku zdjęcia. (Test: ```curl -X POST -F "file=@<plik>.<rozszerzenie>" http://localhost:5000/tasks/upload)```
- GET	localhost:5000/tasks/process-url	Pobranie i analiza zdjęcia z linku URL (?url=<url>).
- GET	localhost:5000/tasks/process-local/<file>	Analiza pliku lokalnego z serwera.

#### RabbitMQ

u: guest

p: guest

localhost:15672

#### Skrypt wysyłający 1000 zapytań

stress_test.py
