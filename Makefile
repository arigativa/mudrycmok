.PHONY: run

# Variables
TG_TOKEN='7271385665:AAFjP5jcWEMORWceDRQycEdJjJ_kjpbI1-0'
MODEL_PATH='/Users/rob/workspace/ml_models/Meta-Llama-3-8B-Instruct-Q6_K.gguf'
INS_STORAGE_PATH='./faiss_db'
EMB_MODEL_PATH='/Users/rob/workspace/chat_atomic/models--intfloat--multilingual-e5-large/snapshots/ab10c1a7f42e74530fe7ae5be82e6d4f11a719eb'

# Default target
run:
	@echo "Running chat.py with specified environment variables..."
	TG_TOKEN=$(TG_TOKEN) \
	MODEL_PATH=$(MODEL_PATH) \
	INS_STORAGE_PATH=$(INS_STORAGE_PATH) \
	EMB_MODEL_PATH=$(EMB_MODEL_PATH) \
	python chat.py