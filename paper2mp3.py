"""
Project: paper2mp3
Converts a paper (pdf) to mp3
Author:  Tiago Tamagusko <tamagusko@gmail.com>
Version: 0.1 (2020-09-25)
License: MIT

Use: edit path and raw_file on line 24-25
Out: paper_audio.mp3 (in project folder)
"""
import re
from io import StringIO
from timeit import default_timer as timer

from gtts import gTTS
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# config
path = ""
raw_file = "paper.pdf"


def pdf2text(path):
    """Converts the PDF to text
    Based on the implementation developed by:
    https://pdfminersix.readthedocs.io/en/latest/tutorial/composable.html
    """
    output_string = StringIO()
    with open(path, "rb") as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return output_string.getvalue()


def to_audiobook(paper):
    """Converts the text (paper) to mp3
    Based on the implementation developed by:
    https://github.com/kjanjua26/HearPapers
    """
    paper_body = []
    text_of_the_paper = pdf2text(paper)
    # use content between post-abstract and pre-references as text
    try:  # If Abstract 
        pre_abs, post_abs = text_of_the_paper.split("Abstract")
    except ValueError: # If ABSTRACT 
        pre_abs, post_abs = text_of_the_paper.split("ABSTRACT")
    pre_refs, post_refs = post_abs.split("References")

    for ix, line in enumerate(pre_refs.split("\n")):
        if len(line) > 15:  # line length above 15 takes as content.
            paper_body.append(line)

    body = " ".join([x for x in paper_body])
    # remove hyphen
    body = body.replace("- ", "")
    # removes citations and texts in parentheses
    body = re.sub("[\(\[].*?[\)\]]", "", body)
    speech = gTTS(text=body, lang="en", slow=False)
    speech.save("paper_audio.mp3")


if __name__ == "__main__":
    start_timer = timer()
    print("pdf -> mp3...")
    to_audiobook(path + raw_file)
    end_timer = timer()
    delay = end_timer - start_timer
    print("Elapsed time: {:0.2f}s\n----\nFile processed! :)".format(delay))
