import os
import webbrowser
from pyuploadcare import Uploadcare
from fpdf import FPDF
import os
from dotenv import load_dotenv

load_dotenv()
public_key = os.getenv("UPLOADCARE_PUBLIC_KEY")
secret_key = os.getenv("UPLOADCARE_SECRET_KEY")

class PdfReport:
    """
    Object that contains information about a pdf report and generates it
    """

    def __init__(self, filename):
        self.filename = filename

    def generate(self, flatmate1, flatmate2, bill):

        pdf = FPDF("P", "pt", "A4")
        pdf.add_page()
        pdf.image(os.path.realpath("house.png"), w=30, h=30)
        pdf.set_font("Times", "B", 16)
        pdf.cell(0, 40, "Flatmate Bill For Period " + bill.period, 0, 1, "C")

        pdf.set_font("Times", "B", 14)
        pdf.cell(200, 40, "Flatmate", 1, 0, "C")
        pdf.cell(200, 40, "Days in house: ", 1, 0, align="C")
        pdf.cell(100, 40, "Amount: ", 1, 1, align="C")

        pdf.set_font("Times", "B", 12)
        pdf.cell(200, 25, flatmate1.name, 1, 0, "C")
        pdf.cell(200, 25, str(flatmate1.days_in_house), 1, align="C")
        pdf.cell(100, 25, str(flatmate1.pays(bill, flatmate2)), 1, 1, align="C")

        pdf.cell(200, 25, flatmate2.name, 1, align="C")
        pdf.cell(200, 25, str(flatmate2.days_in_house), 1, align="C")
        pdf.cell(100, 25, str(flatmate2.pays(bill, flatmate1)), 1, 1, align="C")

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        pdf.output(self.filename)
        # webbrowser.open('file://',os.path.realpath(self.filename))


class FileSharer:
    def __init__(self, filepath, public_key, secret_key):
        self.filepath = filepath
        self.public_key = public_key
        self.secret_key = secret_key

    def share(self):
        uploadcare = Uploadcare(public_key=self.public_key, secret_key=self.secret_key)
        with open(self.filepath, "rb") as file_object:
            ucare_file = uploadcare.upload(file_object)
        filelink = ucare_file.cdn_url
        return filelink
