# [Basics]
import os, pathlib, hashlib, heapq, json
from typing import Optional, Literal
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

# [Ingestion]
import PyPDF2, unstructured

# [LangChain]
from langchain_core.documents import Document

# [LangGraph]

class modularRAG:
    def __init__(
            self,

            # RAG Core Args
            method: Literal["deep_agent", "basic_rag"] = "basic_rag", web_search: bool = True, chat_as_vdb: bool = True, re_ranking:bool = True, grading_step:bool = True,
            static_path:pathlib.Path = None, temp_path:pathlib.Path = None, # Assign temp path later as relative pathing

            # RAG Quality Args
            # [DEFAULTS]
            chunk_size:int = 400, chunk_overlap:int = 50, retrieval_method: Literal["sparse", "dense", "hybrid"] = "hybrid",
            text_splitter: Literal["document_based", "recursive_Character"] = "recursive_Character",

            # RAG QOL Args
            streaming: bool = True,
        ):
        # Initialising Args into Vars
        self.static_path = static_path
        self.temp_path = temp_path
        # Synchronus Tasks Below
        None
        # Multi-Processing Tasks Below
        # Will MP this later
        self.doc_loader()

    def doc_loader(self):
        # To implement: batching, takes all file types as input, use batching
        # get doc's loc (can be temp path made by the code) -> load location of all the files -> batch divide (I need to find a good batch size, equally dividing it over 10 threads sounds fine) -|
        # |-> multiprocess/async(read based on file type + assign metadata (hash) -> convert to json / .md (need to look up the specifics) -|
        # |-> Make a tracker file that checks against the files to make sure a re-read isn't happening (compare hash as well as time modified against the one in the file)-> append to storage object)
        
        if self.static_path is not None:
            doc_loc = pathlib.Path(self.static_path)
        elif self.temp_path is not None:
            doc_loc = pathlib.Path(self.temp_path)
        else:
            EC = "Error - No path defined to work on"
            print(EC)
            return EC

        # Loads pre-existing cache file in process_cache.json
        with open("process_cache.json", "r") as file:
            self.process_cache = json.load(file)
            # print(process_cache)

        files = [
            {
                "file_path":f, 
                "file_size":f.stat().st_size, 
                "time_last_change":f.stat().st_ctime, 
                "time_last_modification":f.stat().st_mtime,
                # TODO : Make the Hash of the file once it's been read
                # "file_hash": hashlib.file_digest(f, "sha256")
            } for f in doc_loc.iterdir() if f.is_file() and "placeholder" not in str(f)] 
        total_files = len(files)

        # Exclusion + Updating Logic (Multiprocessing this for time efficiency, in case of large numbers)
        cache_lookup = {str(item["file_path"]): item for item in (self.process_cache or [])}
        with ProcessPoolExecutor() as executor:
            files_to_process = list(executor.map(self.file_needs_update, files, [cache_lookup] * len(files)))

        print(files_to_process)

        # print(files)

        batched_files = self.batcher(list_of_files=files)
        # print(batched_files)

        # with ProcessPoolExecutor() as executor:
        #     executor.map()

        # docs.append(
        #     Document(page_content=response.text, metadata={"source": source})
        # )

        return

    def file_needs_update(self, file_data:dict = None, cache_lookup:dict = None):
        file_path = str(file_data["file_path"])
        cached_entry = (cache_lookup or {}).get(file_path)
        if cached_entry is not None:
            print(f"File {file_path} already exists in cache, checking if it has been updated since...")
            if file_data.get("file_hash"):
                # compare hashes
                pass
            elif file_data["file_size"] != cached_entry["file_size"] or file_data["time_last_change"] != cached_entry["time_last_change"] or file_data["time_last_modification"] != cached_entry["time_last_modification"]:
                print("no")
            return None
        else:
            return file_data

    def batcher(self, list_of_files: list = None):
        # Creates batches based on file size and divides it based on the total core count of the user's CPU along with multiprocess pooling
        usable_cpu_count = os.cpu_count()-2
        print(usable_cpu_count)

        # load list of dicts and and separate them into batches (size of file accumulated over X total cores)
        files_sorted = sorted(list_of_files, key=lambda f: f["file_size"], reverse=True)
    
        heap = [(0, i) for i in range(usable_cpu_count)]
        heapq.heapify(heap)
        
        assignments = {i: [] for i in range(usable_cpu_count)}
        
        for i in files_sorted:
            file_path = i["file_path"]
            size = i["file_size"]
            load, core_id = heapq.heappop(heap)
            assignments[core_id].append(i)
            heapq.heappush(heap, (load + size, core_id))
        
        return assignments

    def read_files(self, file_data:list = None):
        # Reads all the files and return plain text, delegates reading to read_file, with no "s", this function just opens up the list and passes the file_loc
        for i in file_data:
            output_text = self.read_file(i["file_path"])

    def read_file(self, file_loc:pathlib.Path = None):
        # Does the actual reading, done for the sake of modularisation and code-upkeep
        None

    def read_pdf(self):
        # Includes vector and non-Vector PDF's (non vector and embedded images will route to a read_image func)
        None

    def read_doc(self):
        None

    def read_excel(self):
        None

    def read_md(self):
        None

    def read_json(self):
        None

    def read_code(self):
        None

    def read_img(self):
        None 

    def text_splitter(self):
        None

#__main__
if __name__ == "__main__":
    #TODO: This depends on where the file is being executed from, will need to change in the final edit
    RAG = modularRAG(static_path=r"/home/poyboi/VSCodesWSL/projects/AI.TLDR/input_folder")
    # RAG = modularRAG(static_path=r"../input_folder")