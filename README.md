LLM с которой модель была протестирована можно найти и скачать по этой ссылке:  
https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF  


Для настройки окружения любого из приложений запустите:  
```bash
pip install -r requirements.txt
```


Для запуска telegram-бота вам нужно экспортировать переменнную окружения `TG_TOKEN`.  

```bash
export TG_TOKEN='YOUR TOKEN'
```
и затем запустить приложение с помощью команды make:  
```bash
make run_chat
```

для запуска экспорта инструкций в векторное хранилище вам нужно экспортировать две переменные окружения:  
```bash
export INSTRUCTIONS_DIR_PATH='path to folder with instructions pdf files' 
export STORAGE_OUTPUT_DIR_PATH='folder path to write faiss index to'
```
и затем запустить приложение с помощью команды make:  
```bash
make run_parser
```