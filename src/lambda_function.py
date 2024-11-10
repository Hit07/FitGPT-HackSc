import json

import requests

HEVY_API_URL = "https://api.hevyapp.com/v1/workouts"
# FIREBASE_DB_URL = "https://hackscfitgpt-default-rtdb.firebaseio.com/"
FIREBASE_DB_URL = "https://dsci551-hw1-0-default-rtdb.firebaseio.com/data.json"
"""
Lambda Functionality:
1. On the lambda event, we get a get a data push from the health Auto Export app 
containing body measurements captured from the Apple Health app.
2. Once we get the lambda event, we call the Hevy App API to get workout measurements
3. We combine both this data into one unified json and push to firebase
"""


def lambda_handler(event, context):
    try:
        # Extract the body from the event
        body = event['body']
        body_measurements = body['data']['metrics']

        response = requests.get(HEVY_API_URL, headers={'api-key': '9fa00de0-52aa-43c0-9f8c-7388e56c2fd2'})
        if response.status_code == 200:
            hevy_response = response.json()
            workouts = hevy_response['workouts']
        else:
            print(f"Error calling Hevy API\n {response.text}")
            raise Exception

        aggregated_user_data = {
            "bodyMeasurements": body_measurements,
            "workoutHistory": workouts
        }

        firebase_response = requests.put(FIREBASE_DB_URL, json=aggregated_user_data)
        if firebase_response.status_code == 200:
            return {
                'statusCode': 200,
                'message': "Pushed health data to firebase"
            }
        print(f"Failed writing to Firebase. status_code={firebase_response.status_code}")
        raise Exception
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
