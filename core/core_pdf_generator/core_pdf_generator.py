import io
from reportlab.pdfgen import canvas

START_Y_POSITION = 800
STARTING_X_POSITION = 35


class GeneratePdf:
    def __init__(self):
        self.data_buffer_for_pdf = io.BytesIO()
        self.pdf_writer = canvas.Canvas(self.data_buffer_for_pdf)

    def show_page(self):
        self.pdf_writer.showPage()

    def save_page(self):
        self.pdf_writer.save()

    def set_text(self, text: str):
        self.pdf_writer.drawString(self.pdf_writer._x, START_Y_POSITION, text)

