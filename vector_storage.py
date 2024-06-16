from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


class VectorStorage:
    def __init__(self, storage: FAISS) -> None:
        self.storage: FAISS = storage

    def search(self, query: str) -> str:
        """
        Get user's query and retrieve 2 documents with the lowest score (closest vectors to the query vector).
        Concate the content of the 2 docs into one string.
        """
        results_with_scores = self.storage.similarity_search_with_score(query, k=2)

        base_info = []
        for doc, score in results_with_scores:
            base_info.append(doc.page_content)

        return "\n".join(base_info)


def load_vector_storage(storage_path: str) -> VectorStorage:
    hfe = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
    faiss_instance = FAISS.load_local(
        storage_path, embeddings=hfe, allow_dangerous_deserialization=True
    )

    return VectorStorage(faiss_instance)
