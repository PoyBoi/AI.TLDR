# VLLM - qwen3:14b q_4k_m / AWQ

# Instantiation
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import subprocess

# ENV Defition

class llm_inference(
    
):
    def __init__(self):
        commands = """
VLLM_ATTENTION_BACKEND=XFORMERS \
VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=0 \
TORCH_CUDA_ARCH_LIST=12.0 \
CUDA_VISIBLE_DEVICES=0 \
vllm serve ~/models/Qwen3-14B-AWQ --max-model-len 3500 --gpu-memory-utilization 0.90 --dtype float16 --enforce-eager --port 8000
"""
        self.init_VLLM(commands)

    def init_VLLM(self, commands):
        result = subprocess.run(commands, shell=True, text=True, capture_output=True)
        return result

    def init_LLM(
            self, 

            # Launch Settings
            inference_server_url:str = "http://localhost:8000/v1",
            api_key:str = "something",
            model_location:str = "/home/poyboi/models/Qwen3-14B-AWQ",
            
            # Model Settings
            max_tokens:int = 5, temperature:int = 0,
        ):
        self.llm = ChatOpenAI(
            model = model_location,
            api_key = api_key,
            base_url = inference_server_url,

            # Model Settings
            # max_tokens=max_tokens,
            temperature=temperature,
        )
    
    def LLM_inference(
            self, 

            # Chat Settings
            system_prompt: str = "You are a helpful all-knowing agent.",
            user_prompt: str = "Tell me about the weather today",
            chat_history: list = [],
        ):

        # Invocation

        # Need to add a pathway for history
        if not chat_history:
            messages = [
                SystemMessage(content=system_prompt), HumanMessage(content=user_prompt),
            ]
            response = self.llm.invoke(messages)
        else:
            response = "This functionality (Chat History) has not yet been implemented. Please contact the dev team if this shows up in prod."

        return response

if __name__ == "__main__":
    llm_inf = llm_inference()
    llm_inf.init_VLLM()
    response = llm_inf.init_LLM()

    print(response.text)