from langchain_community.document_loaders import TextLoader


def load_documents():

    loader = TextLoader(
        "documents/company_handbook.txt",
        encoding="utf-8"
    )

    documents = loader.load()

    return documents