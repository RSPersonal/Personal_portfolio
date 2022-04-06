from fpdf import FPDF
from ...helpers_and_validators import input_validator


class TestPDF:
    def __init__(self, title, test, text, pdf, font):
        self.title = title
        self.test = test
        self.text = text
        self.pdf = FPDF()
        self.font = font

    def set_text(self, text: str):
        """
        @param text: 
        @return: 
        """
        if input_validator_helper.value(text):
            self.pdf.cell(40, 10, text)
