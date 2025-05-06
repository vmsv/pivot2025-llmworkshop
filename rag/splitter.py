from langchain_text_splitters import RecursiveCharacterTextSplitter, PythonCodeTextSplitter # type: ignore
from utils import *
import pprint as pp
# check the full list of splitters here
# https://python.langchain.com/v0.2/api_reference/text_splitters/index.html

class MySplit():
    def __init__(self) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
                            chunk_size=1024,
                            chunk_overlap=124,
                            length_function=len,
                            is_separator_regex=False,
                        )

        self.pythonsplitter = PythonCodeTextSplitter() 

    def split_pcode(self, in_code)->list:
        return self.split_text(in_code, "python")

    def split_text(self, in_data:str, in_type:str="text") -> list:
        if in_type =="python":
            return self.splitter.split_text(in_data)
        else:
            return self.splitter.split_text(in_data)


if __name__ == "__main__":
    spliter = MySplit()
    mpdata = getMoonPeek()
    code = getCode()
    pp.pprint(f"Text: {mpdata}\n\n\nChunks: {spliter.split_text(mpdata)}", width=100)
    pp.pprint(f"Code: {code}\n\n\nChunks: {spliter.split_pcode(code)}", compact=False, depth=1)