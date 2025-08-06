import os
import requests

def get_chatgpt_response(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    r = requests.post(url, headers=headers, json=data)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def post_to_teams(message):
    webhook = os.environ["TEAMS_WEBHOOK_URL"]
    requests.post(webhook, json={"text": message}).raise_for_status()

if __name__ == "__main__":
    prompt = os.getenv("CHAT_PROMPT", "Qual o status da última DI?")
    resposta = get_chatgpt_response(prompt)
    post_to_teams(resposta)
