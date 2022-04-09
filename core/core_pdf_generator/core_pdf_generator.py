import io
import reportlab
from reportlab.pdfgen import canvas


class GeneratePdf(canvas):
    def __init__(self):
        self.pdf_writer = canvas.Canvas(self.buffer)

    def show_page(self):
        self.pdf_writer.showPage()

    def save_page(self):
        self.pdf_writer.save()

