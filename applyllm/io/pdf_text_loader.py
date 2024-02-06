import sys, os, glob
from pypdf import PdfReader
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
            
            
#     # @multifunction(None, int)
#     def read_pdf(self, file_idx: int) -> str:
#         """convenient method to read the file index
#         """
#         if (file_idx < len(self.file_path_list)):
#             return read_pdf(str(self.file_path_list[file_idx]))
#         else:
#             return ""
        
#     # @multifunction(None, int)   
#     def count_token(self, file_idx: int)-> int:
#         """convenient method to count token by the file index
#         """
#         if (file_idx < len(self.file_path_list)):
#             return count_token(str(self.file_path_list[file_idx]))
#         else:
#             return 0