# chat_client.py
from openai import OpenAI
from src.prompt_string import response as backend_response

# Initialize the client
client = OpenAI(
    api_key="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")


def get_chat_completion(prompt, model="gpt-4-turbo-preview"):
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


def main():
    # Test translation
    response = get_chat_completion(
        "Translate into Spanish: As a beginner data scientist, I'm excited to learn about OpenAI API!"
    )
    print("Translation:", response)

    # Main code
    # if backend_response:
    #     output_openai = get_chat_completion(backend_response)
    #     print("Main output:", output_openai)


if __name__ == "__main__":
    main()