import openai
import requests
import google.auth
from google.auth.transport.requests import Request
from src.prompt_string import response as backend_response

# Initialize OpenAI client
openai.api_key = "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"

# YouTube API Credentials
CLIENT_ID = "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com"
CLIENT_SECRET = "d-FL95Q19q7MQmFpd7hHD0Ty"
REFRESH_TOKEN = "1//06v6yjoUnWZPICgYIARAAGAYSNwF-L9Irw65ixp_CYTuQtqnDo6Tn55eCo0nbC0ArDkN2HVC8arulfJWfjVbkEbuFo-OY4AYc2RM"


# OAuth 2.0 setup to get YouTube access token
def get_youtube_access_token():
    """Get access token using the refresh token."""
    url = 'https://oauth2.googleapis.com/token'
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    }
    response = requests.post(url, data=payload)
    access_token = response.json().get("access_token")
    return access_token


# Get YouTube Video Recommendations
def get_youtube_videos(query, access_token):
    """Fetch YouTube video recommendations using the YouTube Data API v3."""
    url = "https://www.googleapis.com/youtube/v3/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 3  # Get top 3 recommendations
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        video_data = response.json()
        videos = []
        for item in video_data.get('items', []):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({"title": title, "url": video_url})
        return videos
    else:
        print(f"Error fetching YouTube videos: {response.status_code}")
        return []


# Fetch ChatGPT response for workout details (Updated for OpenAI 1.0+)
def get_chat_completion(prompt):
    try:
        # Create a message as required by the API
        messages = [{"role": "user", "content": prompt}]

        # Call the OpenAI API using the new method
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # Make sure to use the correct model for your use case
            messages=messages
        )

        # Return the content of the first response choice
        return response.choices[0].message['content'] if response.choices else None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def main():
    # Example prompt for ChatGPT
    prompt = "Describe a beginner workout that avoids upper body strength training due to soreness."

    # Get OpenAI response (workout details)
    response = get_chat_completion(prompt)
    if response is None:
        print("OpenAI Response is None. Exiting...")
        return

    print("OpenAI Response:", response)

    # Get YouTube access token
    access_token = get_youtube_access_token()

    # For each workout, get video recommendations from YouTube
    for workout in workout_data:
        workout_name = workout['workout_name']
        advice = workout['advice_or_insights']

        # Create query string using workout name and advice
        query = f"{workout_name} {advice}"

        # Get recommended YouTube videos
        videos = get_youtube_videos(query, access_token)

        # Display results
        print(f"\nRecommended YouTube videos for '{workout_name}':")
        for video in videos:
            print(f"Title: {video['title']}")
            print(f"URL: {video['url']}")
            print()


if __name__ == "__main__":
    main()