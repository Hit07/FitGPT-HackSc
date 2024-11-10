import streamlit as st
import openai
import requests

# OpenAI API Setup
openai.api_key = "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"  # Replace with your OpenAI API key

# Firebase URL for Realtime Database
firebase_url = 'https://hackscfitgpt-default-rtdb.firebaseio.com/data.json'  # Your Firebase Realtime Database URL

# Fetch data from Firebase using requests
def fetch_data_from_firebase():
    response = requests.get(firebase_url)
    
    if response.status_code == 200:
        user_data = response.json()  # This will return the JSON data from Firebase
        return user_data
    else:
        return {"injury": "No Injury", "previous_workout": "Push-up"}

# Function to create a prompt for OpenAI based on Firebase data
def create_openai_prompt(user_data):
    injury = user_data.get('injury', 'No Injury')
    previous_workout = user_data.get('previous_workout', 'Push-up')

    prompt = f"""
    Based on the user's previous workout ('{previous_workout}') and their injury ('{injury}'), suggest an optimal workout plan. 
    Provide detailed instructions, duration, precautions, and how to do each exercise safely considering the injury.
    """
    return prompt

# Function to interact with OpenAI API
def get_openai_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose a different model if needed
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()

# Streamlit UI
st.title("FitGPT - Personalized Workout Suggestions")

# Fetch data from Firebase
user_data = fetch_data_from_firebase()

# Display fetched data (You can customize this based on actual user data from Firebase)
st.write(f"User's Injury: {user_data.get('injury', 'No Injury')}")
st.write(f"Previous Workout: {user_data.get('previous_workout', 'Push-up')}")

# Create a prompt for OpenAI
prompt = create_openai_prompt(user_data)

# Display the prompt for reference
st.write("Generated Prompt for OpenAI:", prompt)

# Get response from OpenAI
openai_response = get_openai_response(prompt)

# Display OpenAI's response
st.header("OpenAI's Workout Suggestions:")
st.write(openai_response)
