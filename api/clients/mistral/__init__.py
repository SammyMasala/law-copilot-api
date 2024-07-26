from api.clients.mistral.client import init_mistral_client

class MistralClient:
    def __init__(self, api_key):
        self.client = init_mistral_client(api_key=api_key)

    def chat_response(self, model, messages):
        try:
            context_messages = []
            for message in messages:
                context_messages.append({"role": ("user" if message.get("isUser") is True else "assistant"), "content": message.get("message")})
            response = self.client.chat(model=model, messages=context_messages)
            print(response)
            return response.choices[0].message.content
        except Exception:
            raise

