import logging

from llama_cpp import Llama
import llm
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# FIXME: read from env variable
TOKEN = "7271385665:AAFjP5jcWEMORWceDRQycEdJjJ_kjpbI1-0"


class ChatHandler:
    def __init__(self, llm_instance: Llama) -> None:
        self.llm = llm_instance

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
        )

    async def respond(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = llm.create_user_message(update.message.text)
        completion = llm_instance.create_chat_completion([user_message], stop=[])

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=llm.get_text(completion),
        )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    llm_instance = llm.initLLM()

    chat_handler = ChatHandler(llm_instance)

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", chat_handler.start)
    application.add_handler(start_handler)

    message_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), chat_handler.respond
    )
    application.add_handler(message_handler)

    application.run_polling()
