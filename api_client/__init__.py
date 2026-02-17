import requests


BASE_URL = "http://localhost:8080/api"
def fetch_course_stats(course_id):
    notes = requests.get(f"{BASE_URL}/grades/stats/data/{course_id}").json()
    response = requests.get(f"{BASE_URL}/courses/{course_id}").json()
    name = response.json().get("courseName",f"Course {course_id}") if response.status == 200 else "Unknown"
    return name, notes