Для настройки окружения вам понадобится pip и python.
Приложение протестировано с python 3.12.3

Для настройки окружения запустите:  
```bash
pip install -r requirements.txt
```

Для запуска приложения вам понадобится LLM.
Страничка LLM с которой приложение было протестировано:  
https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF  
Прямая ссылка на скачивание модели:  
https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct-Q6_K.gguf


Для запуска телеграм-бота вам нужно экспортировать переменнную окружения `TG_TOKEN` и `MODEL_PATH`.  
TG_TOKEN - это токен вашего телеграм-бота  
MODEL_PATH - это путь до LLM  
```bash
export TG_TOKEN='YOUR TOKEN'
export MODEL_PATH='/path/to/your/models/Meta-Llama-3-8B-Instruct-Q6_K.gguf'
```
и затем запустить приложение с помощью команды make:  
```bash
make run_chat
```
Опционально можно экспортировать переменную окружения `INS_STORAGE_PATH` - это путь до папки с индексом векторного хранилища FAISS.


для запуска экспорта инструкций в индекс векторного хранилища вам нужно экспортировать две переменные окружения:  
INSTRUCTIONS_DIR_PATH - путь до папки с pdf файлами инструкций  
STORAGE_OUTPUT_DIR_PATH - путь до папки в которую будут записаны индексы FAISS  
```bash
export INSTRUCTIONS_DIR_PATH='path to folder with instructions pdf files' 
export STORAGE_OUTPUT_DIR_PATH='folder path to write faiss index to'
```
и затем запустить приложение с помощью команды make:  
```bash
make run_parser
```
