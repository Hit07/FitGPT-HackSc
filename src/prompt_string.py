import json

import requests

from exercise_module import process_exercise_data
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
3. The JSON keys must be snake case and not have spaces in between them
4. Always ensure the following JSON keys are used, at any cost DO NOT use any other json keys:
- workout_name
- recommended_sets_and_reps - If the exercise does not involve weight, do not return any weight like 0kg and just return the reps/duration
- exercise
- sets_and_reps
- advice_and_insights
- feedback_on_previous_data
- body_measurement_insight
- display_text
5. The response must be a valid JSON structure ONLY, DO NOT return a list of a singleton object and always adhere to JSON standard and the keys mentioned above
The below is an example JSON of the expected response, follow the JSON schema of the example strictly. (ONLY the schma must be followed not the data). Dont just recommend the same workouts, be reasonable and suggest the right workout
```
{
  "workout_name": "Shoulder & Upper Body Recovery",
  "recommended_sets_and_reps": [
    {
      "exercise": "Arnold Press (Dumbbell)",
      "sets_and_reps": ["12 reps x 6.8kg", "12 reps x 6.8kg", "10 reps x 9.07kg"]
    },
    {
      "exercise": "Lateral Raise (Dumbbell)",
      "sets_and_reps": ["15 reps x 6.8kg", "15 reps x 6.8kg", "15 reps x 6.8kg"]
    },
    {
      "exercise": "Triceps Pushdown",
      "sets_and_reps": ["20 reps x 12.47kg", "15 reps x 12.47kg", "15 reps x 14.74kg"]
    },
    {
      "exercise": "Triceps Extension (Dumbbell)",
      "sets_and_reps": ["20 reps x 9.07kg", "20 reps x 11.34kg", "15 reps x 13.61kg"]
    },
    {
      "exercise": "Lat Pulldown (Machine)",
      "sets_and_reps": ["15 reps x 36.29kg", "12 reps x 36.29kg", "12 reps x 45.36kg"]
    },
    {
      "exercise": "Russian Twist (Bodyweight)",
      "sets_and_reps": ["20 reps x 0kg", "20 reps x 0kg", "20 reps x 0kg"]
    }
  ],
  "advice_and_insights": [
    "Since your shoulders and elbows feel sore, it's best to focus on lighter loads and exercises that don't overstrain these areas. This is why I recommend focusing on shoulder and upper body exercises with moderate weights that allow you to maintain proper form and avoid further strain.",
    "For the Arnold Press, keep the reps lower but work on controlled movements, especially as you increase weight. Your shoulders are prone to strain right now, so careful attention to form is essential.",
    "Lateral Raises should be performed with lighter weights and a controlled tempo, as this exercise directly targets the shoulder area, which is sore. Overloading could aggravate your soreness.",
    "Incorporating a machine-based exercise like the Lat Pulldown will provide better stability for your shoulders and help to reduce strain while still engaging your back and arms.",
    "You will benefit from doing isolation movements like Triceps Extension and Triceps Pushdown to minimize stress on the elbow joint while still working the triceps effectively. These movements also allow you to maintain a lower weight."
  ],
  "feedback_on_previous_data": {
    "overall_analysis": "Your recent activity level is good, with a decent balance between aerobic (step count, walking distance) and anaerobic (strength training) exercises. However, considering the soreness in your shoulders and elbows, it's crucial to listen to your body and avoid pushing too hard on heavy compound exercises today.",
    "body_measurement_insight": "Your current lean body mass of 11lbs is a good sign of muscle development, but the soreness in your upper body indicates that it may be time to focus on active recovery. You also seem to have a relatively low body fat percentage, suggesting a solid foundation for endurance and strength exercises. Today, avoid exercises that heavily tax the upper body to allow your muscles time to recover."
  },
  "display_text": "Today, we will work on upper body recovery and light strength training, focusing on shoulders, arms, and back, while giving your sore elbow and shoulder a break. Keep the movements controlled, and listen to your body as you go through the exercises."
}
```

'''


# print(default_string_start)
# print("Workout History:")
# print(workout_history)
# print("\nExercise Context:")
# print(exercise_context)
# print("\n exercise details:")
# Covert exercise_details to string using json.dumps

# print(exercise_details)
# print("\nRolling Averages:")
# print(avg_data)
# print("\n Feature context:")
# print(description)
# print(default_string_end) concat all of these strings and return them as a response

# print(response)
# You can now use these rolling_averages in your recommendation function


def generate_prompt():
    data = get_firebase_data()
    processed_data = process_firebase_data(data)
    exercise_history = processed_data['exercise_history']
    user_info = processed_data['user_info']
    # Read field_description.txt and print the contents
    with open('field_description.txt', 'r') as file:
        description = file.read()

    workout_history, exercise_context, exercise_details = process_exercise_data(exercise_history)
    response = default_string_start + "\n\nWorkout History:\n" + workout_history + "\n\nExercise Context:\n" + exercise_context + "\n\nExercise Details:\n" + json.dumps(
        exercise_details) + "\n\nRolling Averages:\n" + avg_data + "\n\nFeature context:\n" + description + "\n\n" + default_string_end
    return response, exercise_details
