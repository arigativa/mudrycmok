.PHONY: run_chat run_parser

# Variables with dummy values
MODEL_PATH ?= '../ml_models/Meta-Llama-3-8B-Instruct-Q6_K.gguf'
INS_STORAGE_PATH ?= './faiss_db'


# Default target
run_chat:
	@echo "Running chat.py with specified environment variables..."
	TG_TOKEN=$(TG_TOKEN) \
	MODEL_PATH=$(MODEL_PATH) \
	INS_STORAGE_PATH=$(INS_STORAGE_PATH) \
	python chat.py

run_parser:
	@echo "Running instructions_parser.py with specified environment variables..."
	INSTRUCTIONS_DIR_PATH=$(INSTRUCTIONS_DIR_PATH) \
	STORAGE_OUTPUT_DIR_PATH=$(STORAGE_OUTPUT_DIR_PATH) \
	python instructions_parser.py