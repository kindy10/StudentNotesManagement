from api_client.client import fetch_course_stats
#from
from analytics.engine import calculate_stats,get_interpretation
from visualization.plots import display_histogram

import requests
import numpy as np
import matplotlib.pyplot as plt

def generate_meaning(mean,std,student_no):
    print("\n" + "=" * 40)
    print("INTERPRETATION REPORT")
    print("=" * 40)

    # 1.Analyse de la perfromance globale
    if (mean >= 14):
        performance = 'Excellent'
    elif mean >= 10:
        performance = 'Satisfactory'
    else:
        performance = 'Insufficient'
    print(f"Global performance: {performance} (Average(mean): {mean:.2f})/20")

    if  std < 2 :
        dispersion = "Very homogeneous (The students all have a very similar level)."
    elif std <= 4:
        dispersion = "Balanced (Normal distribution for a class)."
    else:
        dispersion = "Very heterogeneous (Big gap between the best and the worst)."

    print(f": {dispersion}")

    #La regle des 68%(Loi Normale)

    bas = max(0,mean - std)
    haut = min(29,mean +std)
    print(f"Concentration zone: 68% of students fall between {bas:2f} et {haut:2f}")

    if std > 4:
        print("Advice: The teacher should plan groups by level because the gap is too large")
    elif mean < 10:
        print("Advice: The average is low. A general review course is recommended..")
    else:
        print("Advice: The group dynamics are good. Keep it up.")
        print("=" * 40)


def get_course_data(course_id):
    base_url = "http://localhost:8080/api"
    try:
        notes_resp = requests.get(f"{base_url}/grades/stats/data/{course_id}")
        notes = notes_resp.json()
        #Recuperation du nom du cours
        c_info = requests.get(f"{base_url}/courses/{course_id}")
        if c_info.status_code == 200:
            course_name = c_info.json().get("courseName")
        else:
            course_name = f"ID:{course_id}(Non trouve)"
        return notes,course_name
    except Exception as e:
        print(f"Erreur pour le cours {course_id}: {e}")
        return [], f"Erreur ID:{course_id}"

def compare(course_id1,course_id2):
    data1, name1 = get_course_data(course_id1)
    data2, name2 = get_course_data(course_id2)

    if data1 and data2:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), sharey=True)
        # Premier Graphique(Course1)----
        var1 = np.var(data1)
        ax1.hist(data1, bins=10, color='blue', edgecolor='black')
        ax1.axvline(np.mean(data1), color='red', linestyle='--')
        ax1.set_title(f"{name1}\nVariance: {var1:.4f}")
        ax1.set_xlabel('Grade/20')
        ax1.set_ylabel('Number of Students')

        # Deuxieme Graphique(course2)---
        var2 = np.var(data2)
        ax2.hist(data2, bins=10, color='salmon', edgecolor='black')
        ax2.axvline(np.mean(data2), color='yellow', linestyle='--')
        ax2.set_title(f"{name2}\nVariance: {var2:.4f}")
        ax2.set_xlabel('Grade/20')

        plt.suptitle("Comparison of Grade Distribution", fontsize=16)

        # 2 Petite interpretation comparative en console

        print(f"-----Comparison-----")
        if var1 > var2:
            print(f"The course '{name1}' is more heterogeneous than '{name2}.")
        else:
            print(f"The course '{name2}' is more heterogeneous than '{name1}.")

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()
    else:
        print("Error: Make sure you have grades for both courses (ID 1 and 2).")

def raport(course_id = 5):

    url = "http://localhost:8080/api"
    try:
        response = requests.get(f"{url}/grades/stats/data/{course_id}");
        response.raise_for_status()  # verifie si la requete a reussi
        data = response.json()
        try:
            course_info = requests.get(f"{url}/courses/{course_id}").json();
            course_name = course_info.get('courseName', f"Course{course_id}")
        except:
            course_name = f"Course{course_id}"
        if data:
            # Calucls numeriques avec Numpy
            variance = np.var(data)
            standard_deviation = np.std(data)
            mean = np.mean(data)
            generate_meaning(mean, standard_deviation, course_id)
            ##Creation du graphique
            plt.figure(figsize=(10, 6))
            # L'histogramme : bins = 10 divise les notes en 10 tranches
            plt.hist(data, bins=10, color='blue', edgecolor='black', alpha=0.7)

            # Ajout d'une ligne pour la moyenne
            plt.axvline(mean, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean:.2f}')

            plt.title(f'Histogram of Grades for: {course_name}', fontsize=15)
            plt.xlabel('Grade/20')
            plt.ylabel('Number of Students')
            plt.legend()

            # Affichage des stats dans un coin du graphique
            stats_text = f'Standard Deviation: {standard_deviation:.4f}\nvariance: {variance:.4f}'
            plt.gcf().text(0.75, 0.8, stats_text, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

            print(f"\nGraphic generated for {len(data)} students.")
            plt.grid(axis='y', alpha=0.3)
            plt.show()
        else:
            print("No data for this course")
    except Exception as e:
        print(e)

def run_analysis(course_id):
    data,name = fetch_course_stats(course_id)

    if data:
        stats = calculate_stats(data)
        print(f"Analyse for {name}: {get_interpretation(stats)}")

        display_histogram(data,name,stats)
    else:
        print("Data not found for this course!!!")
if __name__ == "__main__":
    #run_analysis(2)
    #compare(5,3)
    #generate_meaning()
    raport()


