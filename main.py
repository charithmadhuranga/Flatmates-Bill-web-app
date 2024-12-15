from datetime import datetime

from flask.views import MethodView
from wtforms import Form
from flask import Flask, render_template, request
from wtforms.fields.simple import StringField, SubmitField
from flatmate_bills.flat import Flatmate, Bill
from flatmate_bills.pdfgenerate import PdfReport,FileSharer,public_key,secret_key


app = Flask(__name__)


class HomePage(MethodView):
    def get(self):
        return render_template("index.html")


class BillFormPage(MethodView):
    def get(self):
        billform = BillForm()
        return render_template("bill_form.html",bill_form=billform)


class ResultPage(MethodView):
    def post(self):
        """Catching the data from the form"""
        formdata = BillForm(request.form)
        amount = float(formdata.amount.data)
        period = datetime.strptime(formdata.period.data.strip(), "%B %Y").strftime("%Y-%m")
        name1 = formdata.name1.data
        days_in_house1 = int(formdata.days_in_house1.data)
        name2 = formdata.name2.data
        days_in_house2 = int(formdata.days_in_house2.data)

        """Flatmate bill calculations and report generation,url sharing"""
        flatmate1 = Flatmate(name1, days_in_house1)
        flatmate2 = Flatmate(name2, days_in_house2)
        bill = Bill(amount, period)
        report_generator = PdfReport(f"{bill.period}.pdf")
        report_generator.generate(flatmate1, flatmate2, bill)
        sharelink = FileSharer(filepath=f"{bill.period}.pdf", public_key=public_key, secret_key=secret_key).share()

        return render_template("result.html",sharelink=sharelink)


class BillForm(Form):
    amount = StringField("Bill Amount:")
    period = StringField("Bill Period: ")
    name1 = StringField("Name: ")
    days_in_house1 = StringField("Days in House: ")
    name2 = StringField("Name: ")
    days_in_house2 = StringField("Days in House: ")
    submit = SubmitField("Calculate")


app.add_url_rule("/", view_func=HomePage.as_view("home_page"))
app.add_url_rule("/bill", view_func=BillFormPage.as_view("bill_form_page"))
app.add_url_rule("/result", view_func=ResultPage.as_view("result_page"))

app.run(debug=True)
