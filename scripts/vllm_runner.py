import subprocess, torch, gc, psutil

# Positioned these two destructive actions outside the creative class
def kill_vllm():
        for proc in psutil.process_iter(['pid', 'name']):
            if "VLLM" in proc.info['name']:
                try:
                    print("Trying to gracefully kill the process")
                    proc.terminate()
                    print("Termination Sucessful")
                except Exception as e:
                    print(f"Termination failed with error: {e}, trying to kill process")
                    proc.kill()

def clear_vram():
    print("Attempting to clear VRAM")
    try:
        gc.collect()
        torch.cuda.empty_cache()
        print("Cleared VRAM safetly")
    except Exception as e:
        print(f"ERROR - Failed to clear VRAM, with error: {e}")

class run_vLLM:
    def __init__(self, commands, restart_vllm: bool = False):
        try:
            if not restart_vllm:
                print("Clearing VRAM")
                clear_vram()
            else:
                print("Killing existing VLLM instance")
                kill_vllm()
            
            self.run_command(commands)
        except:
            print("Failed VLLM launch, destroying process group and retrying init")
            torch.distributed.destroy_process_group()
            clear_vram()
    
    def run_command(self, commands):
        with subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True) as process:
            for line in process.stdout:
                decoded = line.decode('utf8')
                print(decoded, end="")
                if "Application startup complete." in decoded:
                    return