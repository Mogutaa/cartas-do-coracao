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
                "emotional": (
                    "Escreva uma mensagem curta e emocional em português (no máximo 5 linhas), no estilo de WhatsApp. "
                    "Use linguagem informal"
                    "pra parecer real e espontânea. Use emojis com moderação. Tema: "
                ),
            
                "gratitude": (
                    "Escreva uma mensagem curta de gratidão em português (até 5 linhas), como se fosse mandada por WhatsApp. "
                    "Use linguagem simples e carinhosa, e emojis moderados pra parecer escrita real. Tema: "
                ),
            
                "love": (
                    "Escreva uma declaração de amor curta em português (no máximo 5 linhas), no estilo de mensagem de WhatsApp. "
                    "Use um tom fofo e sincero, com erros de digitação naturais e alguns emojis românticos como 💗😻😍, mas sem exagerar. Tema: "
                )
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
