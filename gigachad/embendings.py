from langchain_chroma import Chroma
from langchain_gigachat import GigaChatEmbeddings
from settings import gigachat_key
from utils import split_text_document


def create_embeddings(document):
    embeddings = GigaChatEmbeddings(credentials=gigachat_key, verify_ssl_certs=False)
    documents = split_text_document(document)
    db = Chroma.from_documents(documents=documents, embedding=embeddings)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 10})

    return retriever


init_retriever = create_embeddings("docs/file.txt")
