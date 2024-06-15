import torch
import jinja2
from langchain.vectorstores import faiss
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import pipeline

hfe = HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-large')   # should save local

db = faiss.FAISS.load_local(PATH, embeddings = hfe)

user_template = """
Ты специалист технической поддержки пользователей платформы 1С. Ты помогаешь пользователям решить их проблему.
Пользователь спросил:
```
{{question}}
```
В нашей базе сказано:
```
{{info}}
```
Напиши ответ на вопрос пользователя."""


# TODO get `query` from user

def retrieve_info_from_vectorestore(query: str, db: langchain_community.vectorstores.faiss.FAISS) -> str:
	"""
	Get user's query and retrieve 3 documents with the lowest score (closest vectors to the query vector).
	Concate the content of the 3 docs into one string.
	Args:
		query: string query from user
		db: vectore store
	Returns:
		found_info: string with relevant information
	"""
	results_with_scores = db.similarity_search_with_score(query, k=3)
	base_info = []
	for doc, score in results_with_scores:
	    base_info.append(doc.page_content)
	    found_info = '\n'.join(base_info)

	return found_info


def make_prompt(query: str, info: str) -> str:
	"""
	Use jinja template to render prompt to LLM.
	Args:
		query: user's question
		info: infro retrieved from vectorestore
	Returns:
		prompt: string to pass to LLM
	"""
	query_env = jinja2.Environment()
	query_temp = query_env.from_string(user_template)
	prompt = query_temp.render(question=query, info=info)
	return prompt


