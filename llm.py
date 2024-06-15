from llama_cpp import (
    ChatCompletionRequestAssistantMessage,
    ChatCompletionRequestUserMessage,
    Llama,
    CreateChatCompletionResponse,
    ChatCompletionRequestMessage,
)


# FIXME: pass path to model in env variable
def initLLM() -> Llama:
    return Llama(
        model_path="/Users/rob/workspace/ml_models/Meta-Llama-3-8B-Instruct-Q6_K.gguf",
        n_gpu_layers=-1,  # Uncomment to use GPU acceleration
        seed=1337,  # Uncomment to set a specific seed
        n_ctx=4028,  # Uncomment to increase the context window
    )


def create_user_message(text: str) -> ChatCompletionRequestUserMessage:
    return ChatCompletionRequestUserMessage(role="user", content=text)


def create_assistant_message(text: str) -> ChatCompletionRequestAssistantMessage:
    return ChatCompletionRequestAssistantMessage(role="assistant", content=text)


def get_text(completion: CreateChatCompletionResponse) -> str:
    return completion["choices"][0]["message"]["content"]
