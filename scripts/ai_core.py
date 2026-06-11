# VLLM - qwen3:14b q_4k_m / AWQ

# Instantiation
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

inference_server_url = "http://localhost:8000/v1"

llm = ChatOpenAI(
    model="/home/poyboi/models/Qwen3-14B-AWQ",
    api_key="something",
    base_url=inference_server_url,
    # max_tokens=5,
    temperature=0,
)

system_prompt = "You are a helpful all-knowing agent."
user_prompt = "Tell me how to write a simple python dictionary list code where I can sort based on occurances"

# Invocation
messages = [
    SystemMessage(content=system_prompt), HumanMessage(content=user_prompt),
]
response = llm.invoke(messages)

print(response.text)