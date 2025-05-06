import pypdfium2 as pdfium # type: ignore
import os
import sys

class loadPdf:

    def __init__(self, in_file:str):
        if not os.path.exists(in_file):
            return None

        self.file_path = in_file
        self.pdf = pdfium.PdfDocument(self.file_path)
        
    
    def get_text(self):
        out = list()
        for p in self.pdf:
            out.append(p.get_textpage().get_text_range())
        return ''.join(out)
    
    