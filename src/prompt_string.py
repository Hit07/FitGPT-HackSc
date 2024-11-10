import requests

from src.exercise_module import process_exercise_data
from ten_days_average import avg_data


def get_firebase_data():
    url = "https://hackscfitgpt-default-rtdb.firebaseio.com/data.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching Firebase data: {response.status_code}")
        return None

def process_firebase_data(data):
    processed_data = {}
    processed_data['exercise_history'] = data.get('workoutHistory', [])
    processed_data['user_info'] = {
        'age': data.get('age', 25),
        'gender': data.get('gender', 'male'),
        'fitness_goals': data.get('fitness_goals', ['Bulk up (Get Stronger)'])
    }
    measurements = data.get('body_measurements', {})
    processed_data['body_measurements'] = {
        key: measurements.get(key, []) for key in [
            'weight', 'body_fat_percentage', 'muscle_mass', 'bmi',
            'resting_heart_rate', 'vo2_max', 'step_count'
        ]
    }
    return processed_data



# Main code
data = get_firebase_data()
processed_data = process_firebase_data(data)
exercise_history = processed_data['exercise_history']
user_info = processed_data['user_info']
#Read field_description.txt and print the contents
with open('field_description.txt', 'r') as file:
    description = file.read()

workout_history, exercise_context = process_exercise_data(exercise_history)

default_string_start = '''You are a fitness advisor for an individual, recommending workouts for an individual based on the following factors:
1. Their workout history
2. Their body measurements
3. Their fitness goals
4. Questionnaire answers

Your aim as a fitness advisor is to help the individual to maximize their fitness potential while at the same time minimizing injury and fatigue.


Provide a workout schedule for the next day only with reasoning. 

Questionaire:
1. How are you feeling today ? Any Soreness ?
User Ans: My elbow and shoulders feel a bit sore

2. How is your schedule today ? Is your schedule packed ?
User Ans: Kind of, I need to run a few errands today

3. How much time do you have for a workout today ?
User Ans: 45 mins to 1 hour'''


default_string_end = '''Provide the response in the following format in JSON:
List of:
 - Workout Name I have to do  
 - Lbs x reps (As a list) you recommend 
- Any advice or insights such as reasoning
- Give feedback on the previous data in an analytical manner that the user can keep in mind while working out -- for this look at all the data especially the body measurements data and explain using these metrics
- A display text such as "Today we will work on...."

Note the following while generating the response:
1. Number of exercises must be reasonable and proportional to the number of exercises the user is already working out.
2. Think about the overall volume of the workout, and be reasonable while suggesting this workout for an average individual.
3. The JSON keys must be snake case and not have spaces in between them'''

# print(default_string_start)
# print("Workout History:")
# print(workout_history)
# print("\nExercise Context:")
# print(exercise_context)
# print("\nRolling Averages:")
# print(avg_data)
# print("\n Feature context:")
# print(description)
# print(default_string_end) concat all of these strings and return them as a response

response =  default_string_start + "\n\nWorkout History:\n" + workout_history + "\n\nExercise Context:\n" + exercise_context + "\n\nRolling Averages:\n" + avg_data + "\n\nFeature context:\n" + description + "\n\n" + default_string_end
# print(response)
# You can now use these rolling_averages in your recommendation function


