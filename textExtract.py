from pypdf import PdfReader

class textExtract:
    def __init__(self, pdfName=''):
        self.page = None
        self.pdfName = pdfName

    def readPage(self):
        reader = PdfReader(self.pdfName)
        page = reader.pages[0]

        # extract text in a fixed width format that closely adheres to the rendered
        # layout in the source pdf
        return page.extract_text(extraction_mode="layout")