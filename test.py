from app.rag_pipeline import ask_question

while True:

    question = input("\nAsk a question (or type 'exit'): ")

    if question.lower() == "exit":
        break

    result = ask_question(question)

    print("\nOriginal Query:")
    print(result["original_query"])

    print("\nImproved Query:")
    print(result["improved_query"])

    print("\nAnswer:")
    print(result["answer"])