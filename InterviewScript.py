import requests
import pyttsx3
import speech_recognition as sr

def take_command():
    command = None  
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("listening...")
            listener.adjust_for_ambient_noise(source, duration=0.2)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
    except:
        pass
    return command


def get_data(API_URL, payload, headers):
    engine = pyttsx3.init()
    message = take_command()
    user_prompt = f"Give a concise 1 line introduction about {message}. Keep it brief and informative."

    response = requests.post(API_URL, json=payload, headers=headers)
    # Process the data
    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"]
        print(f"\n{answer}\n")
        engine.say(answer)
        engine.runAndWait()
    else:
        print("error API request failed details", response.text)


def main():
    payload = {
        "model": "openai/gpt-3.5-turbo",  # Change to other models if needed
        "messages": [{"role": "user", "content": user_prompt}],
        "max_tokens": 100,
    }
    API_KEY = "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"
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    user_prompt = f""
    while True:
        get_data(API_URL, payload, headers)


if __name__ == "__main__":
    main()
