from llama_cpp import (
    ChatCompletionRequestAssistantMessage,
    ChatCompletionRequestSystemMessage,
    ChatCompletionRequestUserMessage,
    ChatCompletionResponseMessage,
    Llama,
    CreateChatCompletionResponse,
)

def initLLM(model_path: str) -> Llama:
    return Llama(
        model_path=model_path,
        n_gpu_layers=-1,  # Uncomment to use GPU acceleration
        seed=1337,  # Uncomment to set a specific seed
        n_ctx=4096,  # Uncomment to increase the context window
    )


def create_user_message(text: str) -> ChatCompletionRequestUserMessage:
    return ChatCompletionRequestUserMessage(role="user", content=text)


def create_assistant_message(text: str) -> ChatCompletionRequestAssistantMessage:
    return ChatCompletionRequestAssistantMessage(role="assistant", content=text)


def create_system_message(text: str) -> ChatCompletionRequestSystemMessage:
    return ChatCompletionRequestSystemMessage(role="system", content=text)


def get_response_message(
    completion: CreateChatCompletionResponse,
) -> ChatCompletionResponseMessage:
    return completion["choices"][0]["message"]


def get_response_message_text(completion: CreateChatCompletionResponse) -> str:
    return get_response_message(completion)["content"]
