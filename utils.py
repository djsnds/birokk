from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader


def split_text_document(file_path: str):
    loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=400, separators=["\n\n", "\n", ".", " "]
    )
    splits = text_splitter.split_documents(docs)
    return splits


def extract_data(file_path: str) -> str:
    with open(file_path, encoding="utf-8") as f:
        file_content = f.read()

    return file_content
