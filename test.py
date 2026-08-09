from app.rag_pipeline import ask_question


while True:

    question = input("\nAsk a question (or type 'exit'): ")

    if question.lower() == "exit":
        break

    try:

        result = ask_question(question)

        print("\n" + "=" * 60)

        print("Original Query:")
        print(result["original_query"])

        print("\nImproved Query:")
        print(result["improved_query"])

        print(
            "\nRetrieved Documents:",
            result["retrieved_documents"]
        )

        print(
            "Reranked Documents:",
            result["reranked_documents"]
        )

        print("\nAnswer:")
        print(result["answer"])

        print("=" * 60)

    except Exception as e:

        print("\nError:", e)