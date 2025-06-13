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
            "emotional": "Escreva um texto emocional em português, com muitos erros propositais de digitação, estilo bem brega e exagerado, cheio de emojis românticos 🥺💘😮‍💨, parecendo mensagem de casal grudado no WhatsApp. A mensagem deve parecer espontânea e bem real, como algo que alguém apaixonado escreveria com o coração, falando sobre: ",
            
            "gratitude": "Crie uma mensagem de gratidão em português, com tom leve e carinhoso, cheia de errinhos de escrita e emojis 🥹🙏🏽✨, bem no estilo mensagem de WhatsApp breguinha, como se tivesse sido escrita por alguém simples e grato de verdade, sobre: ",
            
            "love": "Escreva uma declaração de amor em português no estilo beeem brega e apaixonado 😍💗💍, com erros propositais, linguagem de casal de WhatsApp, muitos emojis, jeitinho carinhoso, exagerado, e com drama fofo. Algo do tipo: 'Aii môzin hj nois ja tamo junto faz 10 diiaah 🥺💘 parece pouco mais parece tbm que já eh pra sempreee 💍'. A declaração deve parecer escrita por alguém todo bobo de amor, sobre: "
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
