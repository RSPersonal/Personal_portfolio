""" PDF Generator class

This class creates an instance to write the pdf

TODOS:
1. Fix the X axis when class is created
2. Keep track of correct y and x axis when writing to pdf

"""
import io
from reportlab.pdfgen import canvas

START_Y_POSITION = 800
STARTING_X_POSITION = 35


class GeneratePdf:
    """

    """

    def __init__(self):
        self.data_buffer_for_pdf = io.BytesIO()
        self.pdf_writer = canvas.Canvas(self.data_buffer_for_pdf)

    def show_page(self):
        """
        @return: None
        """
        self.pdf_writer.showPage()

    def save_page(self):
        """
        @return: None
        """
        self.pdf_writer.save()

    def set_text(self, text: str):
        """
        @param text:
        @return: None
        """
        self.pdf_writer.drawString(STARTING_X_POSITION, START_Y_POSITION, text)
