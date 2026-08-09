from app.hybrid_search import hybrid_search


queries = [
    "What is the leave policy?",
    "2FA",
    "DStarix internship",
    "vacation days",
]


for query in queries:

    print("\n" + "=" * 70)

    print("QUERY:", query)

    print("=" * 70)

    results = hybrid_search(query)

    for i, doc in enumerate(results, start=1):

        print(f"\nRESULT {i}")

        print(doc.page_content)