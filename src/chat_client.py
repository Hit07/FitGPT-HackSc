# chat_client.py
import json

import requests
from flask import Flask, jsonify, request

from flask_cors import CORS
from openai import OpenAI
from src.prompt_string import generate_prompt

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

@app.route('/api/heart-data', methods=['POST'])
def main():
    # print(request.get_json())
    # Take the user input and generate a response
    response, exercise_details = generate_prompt()
    if response:
        # data= requests.get('http://127.0.0.1:5000/api/heart-data')
        output_openai = get_chat_completion(response)
        json_data = output_openai.replace("```","").replace("json","").replace("\n","").replace("   ","")
        json_data = json.loads(json_data)
        for ele in json_data['recommended_sets_and_reps']:
            if ele['exercise'] in exercise_details:
                ele['details'] = exercise_details[ele['exercise']]
        # print(data.json())
        # print(json_data)# If response is in JSON format
        # return json_data
        # print("Reached here")
        # print(json_data)

        # print("Main Output:",output_openai)
        return json_data
@app.route('/test')
def test():
    return "Test route working"

if __name__ == "__main__":
    app.run(debug=True)