import logging
import os
import pdfplumber
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def create_vector_storage(
    instructions_dir_path: str, vector_sttorage_out_dir_path: str
) -> None:
    if not instructions_dir_path or not vector_sttorage_out_dir_path:
        logging.error(
            "Please, specify INSTRUCTIONS_DIR_PATH and STORAGE_OUTPUT_DIR_PATH environment variables"
        )
        return

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    hfe = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    file_list = None
    try:
        file_list = os.listdir(instructions_dir_path)
        print("Files in the directory:", file_list)
    except Exception as e:
        print("An error occurred:", e)

    chunks = []
    for file_name in file_list:
        file_path = os.path.join(instructions_dir_path, file_name)
        with pdfplumber.open(file_path) as pdf:
            logging.info(f"reading: {file_path}")
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                # Concatenate text from each page, separated by spaces
                full_text += (page_text + " ") if page_text else ""

            sub_chunks = text_splitter.split_text(full_text)
        chunks.extend(sub_chunks)

    logging.info(f"creating vector storage")
    db = FAISS.from_texts(chunks, hfe)
    logging.info(f"saving vector storage")
    db.save_local(folder_path=vector_sttorage_out_dir_path)


if __name__ == "__main__":
    instructions_path = os.environ.get("INSTRUCTIONS_DIR_PATH")
    storage_output_path = os.environ.get("STORAGE_OUTPUT_DIR_PATH")

    create_vector_storage(instructions_path, storage_output_path)
