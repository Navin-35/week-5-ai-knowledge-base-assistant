from app.rag_pipeline import ask_question


while True:

    question = input("\nAsk a question (or type 'exit'): ")

    if question.lower() == "exit":
        break

    try:

        result = ask_question(question)

        print("\n" + "=" * 60)

        if not result["success"]:

            print("ERROR:")
            print(result["error"])

            continue

        print("Answer:")
        print(result["answer"])

        print("\nSources:")
        print(result["sources"])

        print("\nConfidence:")
        print(result["confidence"])

        print("\nImproved Query:")
        print(result["improved_query"])

        print("=" * 60)

    except Exception as e:

        print("\nUnexpected error:", e)