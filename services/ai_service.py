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
                "emotional": "Escreva uma mensagem emocional em português no estilo de mensagem de WhatsApp. Use linguagem informal, com alguns erros de digitação intencionais (como 'nois', 'te amuh', 'juntin') para parecer espontânea e real. Use emojis com moderação e não exagere na estilização. Tema: ",
            
                "gratitude": "Escreva uma mensagem de gratidão em português no estilo de mensagem de WhatsApp. Use uma linguagem simples e carinhosa, com alguns errinhos naturais de escrita para parecer que foi escrita por uma pessoa real. Use emojis com moderação. Tema: ",
            
                "love": "Escreva uma declaração de amor em português no estilo de mensagem de WhatsApp. Use um tom fofo e sincero, com alguns errinhos de digitação que pareçam naturais (como 'mô', 'pakas', 'diia', 'eh'), sem exagerar. Adicione alguns emojis românticos como 💗😻😍 mas sem colocar em excesso. Tema: "
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
