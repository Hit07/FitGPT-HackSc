from datetime import datetime, timedelta

import requests

OPENSEARCH_ENDPOINT = "https://search-hackscexercisedb-ziw2dlmnimotyfx2lgtjtqfdpy.aos.us-west-2.on.aws"
INDEX_NAME = "exercise_index"
USERNAME = "master"  # Replace with your OpenSearch username
PASSWORD = "Password1234#"  # Replace with your OpenSearch password


def construct_msearch_query(exercise_names):
    """
    Construct the _msearch query body for the given exercise names.
    """
    query_lines = []
    for exercise in exercise_names:
        query_lines.append(f'{{"index": "{INDEX_NAME}"}}')
        query_lines.append(
            '{"query": {"match": {"name": {"query": "' + exercise + '", "fuzziness": "AUTO"}}}, "size": 1}'
        )
    return "\n".join(query_lines) + "\n"


def perform_msearch(query_body):
    """
    Send the _msearch request to OpenSearch and return the results.
    """
    url = f"{OPENSEARCH_ENDPOINT}/_msearch"
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        url, auth=(USERNAME, PASSWORD), headers=headers, data=query_body
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def map_msearch_results(exercise_names, response):
    """
    Map the _msearch response results to the corresponding exercise names.
    """
    results_map = {exercise: None for exercise in exercise_names}
    if response:
        for exercise, result in zip(exercise_names, response["responses"]):
            hits = result.get("hits", {}).get("hits", [])
            results_map[exercise] = hits[0]["_source"] if hits else None
    return results_map


def process_exercise_data(exercise_history):
    """
    Retrieve the exercise data for the past 7 days and process it.
    :param exercise_history:
    :return: (exercises_worked, exercise_context) tuple of strings
    """
    today = datetime.today()
    seven_days_ago = today - timedelta(days=7)

    recent_data = list(
        filter(lambda x: datetime.strptime(x['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') > seven_days_ago,
               exercise_history))
    exercise_names = set([exercise['title'] for day in recent_data for exercise in day['exercises']])
    query_body = construct_msearch_query(exercise_names)
    response = perform_msearch(query_body)
    exercise_details = map_msearch_results(exercise_names, response)
    exercise_context = ""
    for name, details in exercise_details.items():
        exercise_context += f"Name: {name}\nEquipment: {details['equipment']}\nPrimary Muscles:{details['primaryMuscles']}\nSecondary Muscles:{details['secondaryMuscles']}\nCategory:{details['category']}\nLevel:{details['level']}\nMechanic:{details['mechanic']}\nImages:{details['images']}\n"
    exercises_worked = ""
    day_count = 1
    for day in recent_data:
        exercises = day['exercises']
        exercises_worked += f"Exercises for Day {day_count}\n\n"
        for exercise in exercises:
            processed_sets = "\n".join(
                list(map(lambda x: f"{x.get('reps', 'N/A')} reps x {round(x.get('weight_kg', 0), 2)}kg",
                         exercise['sets']))
            )

            exercises_worked += f"Name: {exercise['title']}\nSets:\n{processed_sets}\n"
        exercises_worked += "\n"
        day_count += 1
    return exercises_worked, exercise_context, exercise_details
