from chatbot.utils import load_hallucination_keywords, contains_hallucination
from chatbot.phi_interface import PhiInterface
from chatbot.retriever import DocumentRetriever

class ChatBot:
    def __init__(self, use_documents=True, simplify_questions=False):
        self.use_documents = use_documents
        self.simplify_questions = simplify_questions
        self.chat_history = []
        self.phi = PhiInterface()
        self.retriever = DocumentRetriever() if use_documents else None
        self.hallucination_keywords = []

    async def setup(self):
        self.hallucination_keywords = await load_hallucination_keywords()

    async def ask(self, user_input: str):
        original_input = user_input

        # Optionally simplify the question
        if self.simplify_questions:
            print("🤖 Rephrased Question:", end="", flush=True)
            user_input = await self.phi.simplify_question(user_input)

        # Prepare message history
        messages = [{"role": "system", "content": "Answer concisely and truthfully."}]

        # Add document context if enabled
        if self.use_documents and self.retriever:
            docs = self.retriever.retrieve(user_input)
            if docs:
                context = "\n\n".join(docs)
                messages.append({
                    "role": "system",
                    "content": f"Reference info:\n{context}"
                })

        # Add user query
        messages.append({"role": "user", "content": user_input})

        print("Phi: ", end="", flush=True)
        response = ""

        # Stream the response
        async for chunk in self.phi.stream_response(messages):
            token = chunk['message']['content']
            if contains_hallucination(token, self.hallucination_keywords):
                print("\n🛑 Stopped hallucinated response.\n")
                break
            print(token, end="", flush=True)
            response += token

        # Save full interaction to chat history
        self.chat_history.append((original_input, response))
