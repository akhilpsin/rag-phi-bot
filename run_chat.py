import asyncio
from chatbot.chatbot import ChatBot

async def main():
    doc_mode_input = input("Document mode? (Y/N): ").strip().lower()
    rephrase_input = input("Rephrase questions? (Y/N): ").strip().lower()

    use_documents = doc_mode_input == 'y'
    simplify_questions = rephrase_input == 'y'

    bot = ChatBot(use_documents=use_documents, simplify_questions=simplify_questions)
    await bot.setup()
    print("\n🧠 Chat with Phi — type 'exit' to quit")

    while True:
        question = input("\nYou: ")
        if question.strip().lower() in ["exit", "quit"]:
            break
        await bot.ask(question)

if __name__ == "__main__":
    asyncio.run(main())
