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
                    "Escreva uma mensagem curta e emocional em português (no máximo 3 linhas), no estilo de WhatsApp. "
                    "Use linguagem HIPER informal com erros de digitação intencionais (ex: 'eh', 'mim', 'agente', 'pra sempreh'). "
                    "Adicione 5-7 emojis relevantes de forma orgânica. Inclua expressões coloquiais como 'nois por nois'. "
                    "Misture sentimentos conflitantes (ex: brigas x amor) naturalmente. Tema: "
                ),
                
                "gratitude": (
                    "Escreva uma mensagem curta de gratidão em português (até 3 linhas), como mensagem de WhatsApp. "
                    "Use linguagem EXTREMAMENTE informal com erros propositais (ex: 'tudoh', 'amuh', 'voceh'). "
                    "Inclua 4-6 emojis espalhados naturalmente no texto. Adote um tom íntimo e possessivo (ex: 'é delah/delah'). "
                    "Termine com expressão carinhosa e abreviações. Tema: "
                ),
                
                "love": (
                    "Escreva uma declaração de amor curta em português (máximo 4 linhas), estilo WhatsApp autêntico. "
                    "Use linguagem COLQUIAL com erros naturais (ex: 'completamo', 'sempreh', 'chatinhah'). "
                    "Adicione 6-8 emojis românticos e cotidianos (😍🫵🏽💏🌹💗😏). "
                    "Inclua: 1) Marcador temporal, 2) Fala de terceiros, 3) Confissão imperfeita. Tema: "
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
