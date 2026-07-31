# [Basics]
import os, sys, pathlib
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
        # To implement: batching, takes all file types as input, use async
        # get doc's loc (can be temp path made by the code) -> load location of all the files -> batch divide -|
        # |-> async(read based on file type + assign metadata -> convert to json / .md (need to look up the specifics) -> append to storage object)
        if self.static_path is not None:
            doc_loc = pathlib.Path(self.static_path)
        elif self.temp_path is not None:
            doc_loc = pathlib.Path(self.temp_path)
        else:
            EC = "Error - No path defined to work on"
            print(EC)
            return EC

        files = [f for f in doc_loc.iterdir() if f.is_file() and "placeholder" not in str(f)] 
        # print(files)

        # docs.append(
        #     Document(page_content=response.text, metadata={"source": source})
        # )

        return

    def text_splitter(self):
        None

#__main__
if __name__ == "__main__":
    #TODO: This depends on where the file is being executed from, will need to change in the final edit
    RAG = modularRAG(static_path=r"/home/poyboi/VSCodesWSL/projects/AI.TLDR/input_folder")
    # RAG = modularRAG(static_path=r"../input_folder")