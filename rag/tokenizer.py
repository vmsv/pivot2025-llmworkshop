import sys
from transformers import AutoTokenizer # type: ignore
from utils import *
import pprint as pp

class mytok():
    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained("/app/jina-embeddings-v3")

    def tokenize(self, in_data:str) -> list:
        return self.tokenizer.tokenize(in_data)
        
if __name__ == "__main__":

    mtok = mytok()
    try:
        text_to_tokenize = sys.argv[1]
        pp.pprint(f"Text: {text_to_tokenize}\n\n\nTokens:{mtok.tokenize(text_to_tokenize)}")
    
    except: 
        mp = getMoonPeek()[:60]
        pp.pprint(f"Text: {mp}\n\n\nTokens:{mtok.tokenize(mp)}")