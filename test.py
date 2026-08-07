from app.retriever import search

docs = search("Leave Policy")

for doc in docs:

    print("=" * 60)

    print(doc.page_content)