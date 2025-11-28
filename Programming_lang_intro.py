import requests

API_KEY = "API_KEY"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def get_data():
    message = input("Enter the programming language you want to know about: ")
    user_prompt = f"Give a concise 2-3 line introduction about {message}. Keep it brief and informative."
    payload = {
        "model": "openai/gpt-3.5-turbo",  # Change to other models if needed
        "messages": [{"role": "user", "content": user_prompt}],
        "max_tokens": 100,
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    # Process the data
    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"]
        print(f"\n{answer}\n")
    else:
        print("error API request failed details", response.text)


if __name__ == "__main__":
    get_data()
