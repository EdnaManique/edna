import os
import requests
import sys

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
    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return "⚠️ Limite de requisições atingido. Tente novamente em alguns minutos."
        raise
    return r.json()["choices"][0]["message"]["content"]

def post_to_teams(message):
    webhook = os.environ["TEAMS_WEBHOOK_URL"]
    requests.post(webhook, json={"text": message}).raise_for_status()

if __name__ == "__main__":
    # Leitura obrigatória de CHAT_PROMPT
    prompt = os.getenv("CHAT_PROMPT")
    if not prompt:
        print("❌ Erro: a variável de ambiente CHAT_PROMPT não está definida.")
        sys.exit(1)

    resposta = get_chatgpt_response(prompt)
    post_to_teams(resposta)
