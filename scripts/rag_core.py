# [Basics]
import os, sys, pathlib
from typing import Optional, Literal

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

            # RAG Quality Args
            # [DEFAULTS]
            chunk_size:int = 400, chunk_overlap:int = 50, retrieval_method: Literal["sparse", "dense", "hybrid"] = "hybrid",
            text_splitter: Literal["document_based", "recursive_Character"] = "recursive_Character",

            # RAG QOL Args
            streaming: bool = True,
        ):
        None

    def doc_loader(self):
        # To implement: batching, takes all file types as input, use async
        # get doc's loc (can be temp path made by the code) -> load location of all the files -> batch divide -|
        # |-> async(read based on file type + assign metadata -> convert to json / .md (need to look up the specifics) -> append to storage object)
        doc_loc = pathlib.Path("")
        # docs.append(
        #     Document(page_content=response.text, metadata={"source": source})
        # )

    def text_splitter(self):
        None

#__main__
if __name__ == "__main__":
    None