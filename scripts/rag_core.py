# [Basics]
import os, pathlib, hashlib, heapq, json, time, tempfile, subprocess
from typing import Optional, Literal
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

# [Ingestion]
import PyPDF2, unstructured, orjson
from docx import Document
from python_calamine import CalamineWorkbook

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
            files_to_process = list(executor.map(self.file_needs_update, files, [cache_lookup] * total_files))

        batched_files = self.batcher(list_of_files=files)

        with ProcessPoolExecutor() as executor:
            processed_files = list(executor.map(self.read_files, batched_files.items()))

        print(processed_files)

        # docs.append(
        #     Document(page_content=response.text, metadata={"source": source})
        # )

        return

    def file_needs_update(self, file_data:dict = None, cache_lookup:dict = None):
        file_path = str(file_data["file_path"])
        cached_entry = (cache_lookup or {}).get(file_path)      # Finding the same entry as the one as which we have

        # Happens when the file exists in the cached file, aka it HAS been read before and is getting re-read
        if cached_entry is not None:
            print(f"File {file_path} already exists in cache, checking if it has been updated since...")

            # Comparing File Hashes first as that's a good way to check if the file's contents have been changed
            if file_data.get("file_hash"):
                if file_data["file_hash"] == cached_entry["file_hash"]:
                    print(f"File hash for file {file_path} is similar and doesn't need an update")
                    return None     # aka file doesn't need re-reading
                else:
                    return file_data        # Returning file to be re-read because the hash is dissimilar aka it has been changed since last read
            
            # Backup delta comparision to make sure the file hasn't been updated, if it has, add it to the list of files to be updated / re-read
            elif file_data["file_size"] == cached_entry["file_size"] or file_data["time_last_change"] == cached_entry["time_last_change"] or file_data["time_last_modification"] == cached_entry["time_last_modification"]:
                print(f"File Modification Data for file {file_path} is similar and doesn't need an update")
                return None         # aka file doesn't need re-reading
            else:
                return file_data        # Returning file to be re-read because the back-up data is dissimilar aka it has been changed since last read

        else:
            # Checks if the file itself even is valid
            if os.path.isfile(file_path):
                return file_data        # Returned where there is no cache'd entry, aka this is the first time the file is being read
            else:
                print(f"File {file_path} does not exist at it's path, please re-check, this file will not be read.")
                return None     # Returned when the file's path is incorrect / corrupted

    def batcher(self, list_of_files: list = None):
        # Creates batches based on file size and divides it based on the total core count of the user's CPU along with multiprocess pooling
        usable_cpu_count = os.cpu_count()-2
        print(f"\nUsable CPU count for this session is: {usable_cpu_count}\n")

        # load list of dicts and and separate them into batches (size of file accumulated over X total cores)
        files_sorted = sorted(list_of_files, key=lambda f: f["file_size"], reverse=True)
    
        heap = [(0, i) for i in range(usable_cpu_count)]
        heapq.heapify(heap)
        
        assignments = {i: [] for i in range(usable_cpu_count)}
        
        for i in files_sorted:
            # file_path = i["file_path"]
            size = i["file_size"]
            load, core_id = heapq.heappop(heap)
            assignments[core_id].append(i)
            heapq.heappush(heap, (load + size, core_id))
        
        return assignments

    def read_files(self, file_data:tuple = None) -> None:
        # Reads all the files and return plain text, delegates reading to read_file, with no "s", this function just opens up the list and passes the file_loc
        core_id, assignments = file_data
        # Q: How to do error handling in MP
        # Q: How to join threads and wait for the slowest / rate limiter step before proceeding
        for file in assignments:
            output_text = self.read_file(file["file_path"])
            file["text_content"] = output_text

        file_data_with_text = {"core_id": core_id, "assignments": assignments}
        return file_data_with_text

    def read_file(self, file_loc:pathlib.Path = None) -> None:
        action_map = {
            ".pdf": self.read_pdf,
            ".docx": self.read_doc,
            ".doc": self.read_doc,
            ".xlsx": self.read_excel,
            ".xls": self.read_excel,
            ".md": self.read_md,
            ".json": self.read_json,
            ".png": self.read_img,
            ".jpg": self.read_img,
            ".jpeg": self.read_img,
            ".webp": self.read_img,
            ".py": self.read_code,
            ".js": self.read_code,
            ".html": self.read_code,
            ".css": self.read_code,
            ".ts": self.read_code,
            ".sh": self.read_code,
            ".bat": self.read_code,
            ".txt": self.read_txt,
            ".ppt": self.read_ppt,
            ".pptx": self.read_ppt,
        }
        # Does the actual reading, done for the sake of modularisation and code-upkeep
        # print(file_loc)
        file_format = "".join(file_loc.suffixes)

        file_read_function = action_map.get(file_format, self.unsupported_file_format)
        return file_read_function(file_loc = file_loc, file_format = file_format)


    def read_pdf(self, file_loc: pathlib.Path = None, file_format: str = None):
        # Includes vector and non-Vector PDF's (non vector and embedded images will route to a read_image func)
        print("Reading PDF...")
        None

    def read_doc(self, file_loc: pathlib.Path = None, file_format: str = None):
        print("Reading DOC/DOCX...")
        if file_format == ".docx":
            doc = Document(file_loc)
            parts = []
            for para in doc.paragraphs:
                if para.text.strip():
                    parts.append(para.text)
            for table in doc.tables:
                for row in table.rows:
                    parts.append("\t".join(cell.text for cell in row.cells))
            return "\n".join(parts)

        elif file_format == ".doc":
            # No reliable pure-python parser for legacy .doc.
            # Convert via headless LibreOffice into a temp dir, then parse as docx.
            with tempfile.TemporaryDirectory() as tmp:
                # TODO: What about people who don't have WSL / Linux to run, I need an alternative method for this
                subprocess.run(
                    ["libreoffice", "--headless", "--convert-to", "docx",
                    "--outdir", tmp, str(file_loc)],
                    check=True, capture_output=True, timeout=120
                )
                converted = pathlib.Path(tmp) / (file_loc.stem + ".docx")
                return self.read_doc(converted)

        else:
            raise ValueError(f"Unsupported extension for read_doc: {file_format}")

    def read_excel(self, file_loc: pathlib.Path = None, file_format: str = None):
        workbook = CalamineWorkbook.from_path(str(file_loc))

        sheets_out = []
        for sheet_name in workbook.sheet_names:
            rows = workbook.get_sheet_by_name(sheet_name).to_python()
            sheet_text = "\n".join(
                "\t".join(str(cell) if cell is not None else "" for cell in row)
                for row in rows
            )
            sheets_out.append(f"# Sheet: {sheet_name}\n{sheet_text}")

        return "\n\n".join(sheets_out)

    def read_md(self, file_loc: pathlib.Path = None, file_format: str = None):
        return file_loc.read_text(encoding="utf-8", errors="replace")

    def read_json(self, file_loc: pathlib.Path = None, file_format: str = None):
        with open(file_loc, "rb") as f:
            data = orjson.loads(f.read())
        # Return both raw text and parsed object if downstream needs structure;
        # here we return pretty text for uniform text-pipeline handling.
        return orjson.dumps(data, option=orjson.OPT_INDENT_2).decode("utf-8")

    def read_code(self, file_loc: pathlib.Path = None, file_format: str = None):
        None

    def read_img(self, file_loc: pathlib.Path = None, file_format: str = None):
        None 

    def read_txt(self, file_loc: pathlib.Path = None, file_format: str = None):
        None

    def read_ppt(self, file_loc: pathlib.Path = None, file_format: str = None):
        None

    def unsupported_file_format(self, file_loc: pathlib.Path = None, file_format: str = None) -> None:
        print(f"Provided file at {file_loc} does not have a valid file format")
        return None

    def text_splitter(self):
        None

#__main__
if __name__ == "__main__":
    #TODO: This depends on where the file is being executed from, will need to change in the final edit
    RAG = modularRAG(static_path=r"/home/poyboi/VSCodesWSL/projects/AI.TLDR/input_folder")
    # RAG = modularRAG(static_path=r"../input_folder")