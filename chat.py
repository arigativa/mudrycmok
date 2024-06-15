import logging
import os
from typing import Iterable

from llama_cpp import ChatCompletionRequestMessage, CreateChatCompletionResponse, Llama
import telegram
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
from vector_storage import load_vector_storage, VectorStorage


class ChatHandler:
    message_history_key = "message_history"

    def __init__(
        self,
        llm_instance: Llama,
        assistant_system_prompt: str,
        instructions_storage: VectorStorage,
    ) -> None:
        self.llm_instance: Llama = llm_instance
        self.system_prompt = llm.create_system_message(assistant_system_prompt)
        self.instruction_storage = instructions_storage

    async def typing(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=telegram.constants.ChatAction.TYPING,
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Здравствуйте, я бот и я здесь чтобы вам помочь!",
        )

    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data[ChatHandler.message_history_key] = [self.system_prompt]

    async def like(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.info("Sending conversation history for preference analysis")

    async def dislike(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.info("Sending conversation history for hatred analysis")

    async def respond(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.typing(update, context)
        user_message_text = update.message.text
        logging.info(f"user: {user_message_text}")

        instruction_search_result = self.instruction_storage.search(user_message_text)
        logging.info(f"search: {instruction_search_result}")

        messages_history = self._update_and_get(
            [
                llm.create_user_message(user_message_text),
                llm.create_system_message(
                    prompts.mk_instructions_search_prompt(instruction_search_result)
                ),
            ],
            context,
        )

        await self.typing(update, context)
        assistant_response = self.llm_instance.create_chat_completion(
            messages_history, stop=[], repeat_penalty=1.1
        )
        assistant_message = llm.get_response_message(assistant_response)
        self._update_and_get([assistant_message], context)

        assistant_message_text = llm.get_response_message_text(assistant_response)
        logging.info(f"assistant: {assistant_message_text}")

        await update.message.reply_text(assistant_message_text)

    def _update_and_get(
        self,
        values: Iterable[ChatCompletionRequestMessage | CreateChatCompletionResponse],
        context: ContextTypes.DEFAULT_TYPE,
    ):
        history: list = context.user_data.get(
            ChatHandler.message_history_key, [self.system_prompt]
        )
        history.extend(values)

        context.user_data[ChatHandler.message_history_key] = history

        return history


def main():
    tg_token = os.environ.get("TG_TOKEN")
    model_path = os.environ.get("MODEL_PATH")
    instructions_storage_path = os.environ.get("INS_STORAGE_PATH")

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    logging.info("loading instructions vector storage")

    vector_storage = load_vector_storage(instructions_storage_path)

    logging.info("instructions vector storage loaded")

    llm_instance = llm.initLLM(model_path)

    chat_handler = ChatHandler(
        llm_instance,
        prompts.assistant_system_prompt,
        vector_storage,
    )

    application = ApplicationBuilder().token(tg_token).build()

    start_handler = CommandHandler("start", chat_handler.start)
    application.add_handler(start_handler)

    reset_handler = CommandHandler("reset", chat_handler.reset)
    application.add_handler(reset_handler)

    like_handler = CommandHandler("like", chat_handler.like)
    application.add_handler(like_handler)

    dislike_handler = CommandHandler("dislike", chat_handler.dislike)
    application.add_handler(dislike_handler)

    message_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), chat_handler.respond
    )
    application.add_handler(message_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
