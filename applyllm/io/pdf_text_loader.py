import sys, os, glob
from pypdf import PdfReader
from typing import Tuple, List
from langchain_core.documents.base import Document


"""
https://pythonhosted.org/multidispatch/
"""
class PDFHelper():
    def __init__(self, data_folder: str, file_pattern: str):
        """
        Args:
          data_folder: where all the pdf files are
          file_pattern: the pdf files match this pattern
          
        Examples:
           
          PDFHelper(data_folder = "./data/medreports", 
                    file_pattern="KK-SCIVIAS-*.pdf")
        """
        self.data_folder = data_folder
        self.file_pattern = file_pattern
        self.dir_path = f"{data_folder}/{file_pattern}"
        self.file_path_list = glob.glob(self.dir_path)
        
    # @multifunction(None, str)
    def read_pdf(self, input) -> str:
        """read from the give path the text and returns a raw string. 
           use print to print the content
        """
        if isinstance(input, str):
            file_path = input
            reader = PdfReader(file_path)
            content_raw_str = "".join([page.extract_text() for page in reader.pages])
            return content_raw_str
        elif isinstance(input, int):
            file_idx = input
            if (file_idx < len(self.file_path_list)):
                return self.read_pdf(str(self.file_path_list[file_idx]))
            else:
                return ""
        else:
            return ""
    
    # @multifunction(None, str)
    def count_token(self, input)-> int:
        """count the total token in a pdf file
        """
        if isinstance(input, str):
            file_path = input
            token_size = len(self.read_pdf(file_path))
            print(f"file: {file_path}\n" + 
              f"total token: {token_size}")
            return token_size
        elif isinstance(input, int):
            file_idx = input
            if (file_idx < len(self.file_path_list)):
                return self.count_token(str(self.file_path_list[file_idx]))
            else:
                return 0
        else:
            return 0
              
    def read_txt(self, input) -> str:
        """read from the give path the text and returns a raw string. 
           use print to print the content
        """
        if isinstance(input, str):
            file_path = input
            with open(file_path, "r") as txt_file:
                content_raw_str = txt_file.read()
            return content_raw_str
        elif isinstance(input, int):
            file_idx = input
            if (file_idx < len(self.file_path_list)):
                return self.read_txt(str(self.file_path_list[file_idx]))
            else:
                return ""
        else:
            return ""
        

class DocMetaInfo():
    def __init__(self, doc: Document):
        self.read_meta(doc)
    
    
    def read_meta(self, doc: Document):
        file_content = doc.page_content
        self.source = doc.metadata['source']
        self.name = self.source.split("/")[-1]
        self.token_size = len(file_content.split())
        self.character_size = len(file_content)
        
        
    def __str__(self):
        """call by print"""
        return f"source:{self.source}\nname:{self.name}\ntokens:{self.token_size}\ncharacters:{self.character_size}"
    
    
    def __repr__(self):
        """convert obj to string, called by jupyter cell"""
        return self.__str__()


class DocCorpusS3(): 
    def __init__(self, data: List[Document]):
        # enumerate returns a key, element tuple, the x[1] is the DocMetaInfo(doc)
        # https://stackoverflow.com/questions/16945518/finding-the-index-of-the-value-which-is-the-min-or-max-in-python/16945868#16945868
        self.docs = data
        self.docs_meta_infos = [DocMetaInfo(doc) for doc in data]
        self.idx_of_max_token, self.max_doc_meta = max(enumerate(self.docs_meta_infos), key=lambda x: x[1].token_size)
        self.idx_of_min_token, self.min_doc_meta = min(enumerate(self.docs_meta_infos), key=lambda x: x[1].token_size)
    

    def get_s3_obj_info(self, idx: int, show_content: bool = False) -> Tuple[Document, DocMetaInfo]:
        if (self.docs is not None):
            n = len(self.docs)
            print(f"total objects: {n}")
            print("="*20)
            if -n <= idx < n: # in range of list idx
                doc = self.docs[idx]
                meta_info = self.docs_meta_infos[idx]
                file_content = doc.page_content
                
                print(f"s3 key     :{meta_info.source}")
                print(f"obj name   :{meta_info.name}")
                print(f"token size :{meta_info.token_size}")
                print(f"char. size :{meta_info.character_size}")
                if show_content:
                    print("-"*20)
                    print(file_content)
            return doc, meta_info
        else:
            return None