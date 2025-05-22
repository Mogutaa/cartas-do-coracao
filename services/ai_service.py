import requests
from config.settings import settings

class AIService:
    @staticmethod
    def get_writing_suggestion(prompt: str, style: str = "emotional"):
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_KEY}",
            "Content-Type": "application/json"
        }

        style_prompts = {
            "emotional": "Escreva um texto emocional e sincero em português que expresse: ",
            "gratitude": "Crie uma mensagem de gratidão detalhada sobre: ",
            "love": "Desenvolva uma declaração de amor profunda com referência a: "
        }

        full_prompt = f"{style_prompts.get(style, '')}{prompt}. Use linguagem natural e pessoal."

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": "qwen/qwen3-14b:free",
                    "messages": [{
                        "role": "user",
                        "content": full_prompt
                    }]
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Erro na API de IA: {str(e)}")
            return None