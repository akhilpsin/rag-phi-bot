import asyncio
import ollama

class PhiInterface:
    def __init__(self, model_name="phi"):
        self.model_name = model_name

    async def stream_response(self, messages, temperature=0.1):
        loop = asyncio.get_event_loop()
        queue = asyncio.Queue()

        def sync_stream():
            for chunk in ollama.chat(model=self.model_name, messages=messages, stream=True, options={"temperature": temperature}):
                asyncio.run_coroutine_threadsafe(queue.put(chunk), loop)
            asyncio.run_coroutine_threadsafe(queue.put(None), loop)

        asyncio.get_event_loop().run_in_executor(None, sync_stream)

        while True:
            chunk = await queue.get()
            if chunk is None:
                break
            yield chunk
    
    async def simplify_question(self, text):
        prompt = f"Rephrase this question in a simple and grammatically correct way: {text}"
        messages = [{"role": "user", "content": prompt}]
        simplified = ""

        async for chunk in self.stream_response(messages):
            token = chunk['message']['content']
            print(token, end="", flush=True)
            simplified += token
        return simplified.strip()
