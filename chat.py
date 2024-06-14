import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)


from llama_cpp import (
    ChatCompletionRequestAssistantMessage,
    ChatCompletionRequestUserMessage,
    Llama,
    CreateChatCompletionResponse,
    ChatCompletionRequestMessage,
)

llm = Llama(
    model_path="/Users/rob/workspace/ml_models/Meta-Llama-3-8B-Instruct-Q6_K.gguf",
    n_gpu_layers=-1,  # Uncomment to use GPU acceleration
    seed=1337,  # Uncomment to set a specific seed
    n_ctx=4028,  # Uncomment to increase the context window
)


TOKEN = "7271385665:AAFjP5jcWEMORWceDRQycEdJjJ_kjpbI1-0"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def create_user_message(text: str) -> ChatCompletionRequestUserMessage:
    return ChatCompletionRequestUserMessage(role="user", content=text)


def create_assistant_message(text: str) -> ChatCompletionRequestAssistantMessage:
    return ChatCompletionRequestAssistantMessage(role="assistant", content=text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = create_user_message(update.message.text)
    completion = llm.create_chat_completion([user_message], stop=[])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=completion["choices"][0]["message"]["content"],
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), respond)
    application.add_handler(message_handler)

    application.run_polling()
