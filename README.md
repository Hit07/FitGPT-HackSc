# FitGPT Backend

### Files
**chat_client.py**: Main Flask application that handles API requests and integrates with OpenAI's GPT model.
**exercise_module.py**: Module for processing exercise data, including querying the OpenSearch database for exercise details.
**lambda_function.py**: AWS Lambda function that aggregates data from Hevy API and Apple Health, then pushes it to Firebase.
**prompt_string.py**: Generates the prompt for the GPT model based on user data and exercise history.

### Setup
- Install dependencies:
```
pip install -r requirements.txt
```

### Set up environment variables:
- ```API_KEY```: Your OpenAI API key
- ```OPENSEARCH_ENDPOINT```: URL for your OpenSearch instance
- ```USERNAME and PASSWORD```: Credentials for OpenSearch
Firebase and Hevy API credentials (see lambda_function.py)
Ensure you have access to the required APIs and databases: 
1. OpenAI GPT-4
2. OpenSearch
3. Firebase Realtime Database
4. Hevy API

### API Endpoints
- /api/heart-data (POST): Main endpoint for generating workout recommendations
- /test (GET): Test route to check if the server is running

### Data Flow
* User health data is sent to AWS Lambda
* Lambda fetches workout data from Hevy API
* Data is aggregated and stored in Firebase
* When a recommendation is requested, data is fetched from Firebase
* Data is processed and sent to OpenAI's GPT model
