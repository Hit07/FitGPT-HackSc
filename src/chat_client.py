# chat_client.py
import json

from flask import Flask, jsonify

from flask_cors import CORS
from openai import OpenAI
from src.prompt_string import response as backend_response

# Initialize the client
client = OpenAI(
    api_key="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")


def get_chat_completion(prompt, model="gpt-4o-mini"):
    try:
        # Creating a message as required by the API
        messages = [{"role": "user", "content": prompt}]

        # Calling the ChatCompletion API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )

        # Returning the extracted response
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend to access backend
CORS(app)

@app.route('/api/heart-data', methods=['GET'])
def main():
    if backend_response:
        output_openai = get_chat_completion(backend_response)
        json_data = output_openai.replace("```","").replace("json","").replace("\n","").replace("   ","")
        print(json_data)
        # json_data = json.loads(json_data)
        # print(json_data)# If response is in JSON format
        # return json_data
        return {
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


if __name__ == "__main__":
    app.run(debug=True)