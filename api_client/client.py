import requests

BASE_URL = "http://localhost:8080/api"
def fetch_course_stats(course_id):
    # 1. Récupérer les notes
    notes_resp = requests.get(f"{BASE_URL}/grades/stats/data/{course_id}")
    notes = notes_resp.json()  # Ici on peut transformer direct si on est sûr

    # 2. Récupérer les infos du cours (C'est ici qu'était l'erreur)
    response = requests.get(f"{BASE_URL}/courses/{course_id}")  # <--- PAS de .json() ici !

    if response.status_code == 200:
        # On extrait le JSON seulement si la requête a réussi
        data_json = response.json()
        # Attention à la casse : "courseName" (minuscule au début) ou "CourseName" ?
        name = data_json.get("courseName", f"Course {course_id}")
    else:
        name = f"Unknown Course {course_id}"

    return notes, name

