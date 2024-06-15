import logging
import os

from llama_cpp import ChatCompletionRequestMessage, CreateChatCompletionResponse, Llama
import llm
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import prompts


class ChatHandler:
    message_history_key = "message_history"

    def __init__(self, llm_instance: Llama, system_prompt: str) -> None:
        self.llm_instance: Llama = llm_instance
        self.system_prompt = llm.create_system_message(system_prompt)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
        )

    async def respond(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message_text = update.message.text
        logging.info(f"user: ${user_message_text}")

        user_message = llm.create_user_message(update.message.text)
        messages_history = self._update_and_get(user_message, context)

        completion_reponse = self.llm_instance.create_chat_completion(
            messages_history, stop=[]
        )

        completion_message = llm.get_response_message(completion_reponse)
        self._update_and_get(completion_message, context)

        completion_message_text = llm.get_response_message_text(completion_reponse)
        logging.info(f"assistant: ${completion_message_text}")

        await update.message.reply_text(completion_message_text)

    def _update_and_get(
        self,
        value: ChatCompletionRequestMessage | CreateChatCompletionResponse,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        history = context.user_data.get(
            ChatHandler.message_history_key, [self.system_prompt]
        )
        history.append(value)

        context.user_data[ChatHandler.message_history_key] = history

        return history


def main():
    tg_token = os.environ.get("TG_TOKEN")
    model_path = os.environ.get("MODEL_PATH")

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    llm_instance = llm.initLLM(model_path)

    chat_handler = ChatHandler(llm_instance, prompts.system_prompt)

    application = ApplicationBuilder().token(tg_token).build()

    start_handler = CommandHandler("start", chat_handler.start)
    application.add_handler(start_handler)

    message_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), chat_handler.respond
    )
    application.add_handler(message_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
