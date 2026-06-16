# Instantiation
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import subprocess, sys, requests, os

# Importing from files
from vllm_runner import run_vLLM, kill_vllm, clear_vram

# ENV Defition
# None

class llm_inference:
    def __init__(self):
        print("Starting INIT process")
        self.model_launch_args = {
            "model_location": "/home/poyboi/models/Qwen3-14B-AWQ", # aka "model_name"
            "max_model_len": 3000,
            "gpu_memory_util": 0.90,
            "dtype": "float16",
            "port": 8000,
            "api_key": "something",
            "max_tokens": 5, 
            "temperature": 0,
            "restart_vllm": True
        }
        self.model_launch_args["inference_server_url"] = f"http://localhost:{self.model_launch_args['port']}/v1"

        vllm_launch_daemon = """
        VLLM_ATTENTION_BACKEND=XFORMERS VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=0 TORCH_CUDA_ARCH_LIST=12.0 CUDA_VISIBLE_DEVICES=0
        vllm serve {model_location} --max-model-len {max_model_len} --gpu-memory-utilization {gpu_memory_util} --dtype {dtype} --enforce-eager --port {port} &
        """.format(**self.model_launch_args)
        
        # Init sequences
        try:
            print("\nUsing Args:\n", self.model_launch_args)
            
            print("1. INIT'ing VLMM"); c_proc = "init vllm"
            if self.model_launch_args["restart_vllm"]:
                print("RESTART'ing vLLM now...")
                run_vLLM(
                    commands = vllm_launch_daemon, 
                    restart_vllm = True
                )
            elif not self.check_vllm_health(port=self.model_launch_args["port"]):
                print("INIT'ing vLLM now...")
                run_vLLM(
                    commands = vllm_launch_daemon
                )

            print(f"Done with {c_proc}")

            print("2. INIT'ing LMM"); c_proc = "init llm"
            self.init_LLM(**self.model_launch_args)
            print(f"Done with {c_proc}")

        except Exception as e:
            print(f"RAN INTO SEVERE ERRORS: {e} during {c_proc}")
            return

    def check_vllm_health(self, port=8000):
        url = f"http://localhost:{port}/v1/models"
        print(f"Trying with URL: {url}")
        try:
            response = requests.get(url, timeout=3)
            print(response, response.status_code, response.connection)
            if response.status_code == 200:
                print("VLLM is up and running")
                return True
            else:
                print(f"ERROR - Server replied with status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            return False

    def run_command(self, commands):
        run_daemon = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        for line in run_daemon.stdout:
            decoded = line.decode("utf8")
            print(decoded, end = "")  # keeping the logs

    def init_LLM(self, **kwargs):
        self.llm = ChatOpenAI(
            model = kwargs["model_location"],
            
            # Model Settings
            api_key = kwargs["api_key"], 
            base_url = kwargs["inference_server_url"],

            # Language Settings
            temperature = kwargs["temperature"],
            # max_tokens = kwargs["max_tokens"],
        )
    
    def LLM_inference(
            self, 

            # Chat Settings
            system_prompt: str = "You are a helpful all-knowing agent.",
            user_prompt: str = "Tell me about the weather today",
            chat_history: list = [],
        ):

        # Invocation
        if not chat_history:
            messages = [
                SystemMessage(
                    content = system_prompt
                ), 
                HumanMessage(
                    content = user_prompt
                ),
            ]
            response = self.llm.invoke(messages)
        else:
            response = "This functionality (Chat History) has not yet been implemented. Please contact the dev team if this shows up in prod."

        return response

if __name__ == "__main__":
    llm_inf = llm_inference()
    user_prompt_run = "What is the meaning of life, answer in one word"
    response = llm_inf.LLM_inference(user_prompt=user_prompt_run)

    print(response.text)
    kill_vllm()