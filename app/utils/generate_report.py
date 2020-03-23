from app.models import User
import io
import os
import re
import datetime
from datetime import datetime
import json
import sys
from flask import current_app
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Image, Paragraph, Spacer, SimpleDocTemplate, Table, TableStyle, LongTable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle as PS
from reportlab.platypus.flowables import TopPadder
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.units import cm, mm, inch
import PIL

class PageNumCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):

        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):

        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):

        page_count = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):

        page = "Page %s of %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 10)
        self.drawRightString(195 * mm, 10 * mm, page)

class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        apply(SimpleDocTemplate.__init__, (self, filename), kw)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))
            if style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))

def generate_report(username, data):

    directory = os.path.join(
        os.path.dirname(current_app.instance_path), f'app/userdata/{username}/reports'
    )

    if not os.path.exists(directory):
        os.makedirs(directory)

    url = directory + '/report_' + username  + '.pdf'


    styles = getSampleStyleSheet()

    ordinary = PS(
        name='ordinary',
        fontName='Helvetica',
        alignment=1,
        fontSize=12,
        leading=14)

    centered = PS(name='centered',
        fontSize=14,
        leading=16,
        alignment=1,
        spaceAfter=10)

    bold = PS(
        name='bold',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=16)

    centered_bold = PS(name='centered_bold',
        fontSize=16,
        fontName='Helvetica-Bold',
        leading=18,
        alignment=1,
        spaceAfter=10)

    h2 = PS(name='Heading2',
        fontSize=12,
        leading=14)


    Report = []


    logo = Image('app/static/images/hse.jpg', 1 * inch, 1 * inch)
    Report.append(logo)
    Report.append(Spacer(1, 12))
    Report.append(Spacer(1, 12))
    Report.append(Paragraph('Coronavirus Statistics, HSE', centered_bold))
    Report.append(Spacer(1, 12))
    Report.append(Spacer(1, 12))
    Report.append(Paragraph(f'Report for user: {username}', centered_bold))
    Report.append(Spacer(1, 12))
    Report.append(Spacer(1, 12))

    curr_time = str(datetime.now()).split(".")[0]
    Report.append(Paragraph(f'Time of Report creation: {curr_time}', centered))


    Report.append(PageBreak())

    styleN = styles['Normal']
    styleN.wordWrap = 'CJK'

    Report.append(Paragraph('COVID-19 Main Live Statistics', centered_bold))

    Report.append(Spacer(1, 12))
    Report.append(Spacer(1, 12))

    total_cases = data['statistics']['total_cases']
    total_deaths = data['statistics']['total_deaths']
    total_recovered = data['statistics']['total_recovered']

    Report.append(Paragraph(f'COVID-19 Total Cases: {total_cases}', bold))
    Report.append(Spacer(1, 12))

    Report.append(Paragraph(f'COVID-19 Total Deaths: {total_deaths}', bold))
    Report.append(Spacer(1, 12))

    Report.append(Paragraph(f'COVID-19 Total Recovered: {total_recovered}', bold))
    Report.append(Spacer(1, 12))
    Report.append(Spacer(1, 12))

    Report.append(Paragraph('COVID-19 Demographics Data:', centered_bold))
    Report.append(Spacer(1, 12))

    data_age = [[Paragraph(cell, styleN) for cell in row] for row in data['demographics']['death_rate_by_age']]
    data_age.insert(0, ["Age", "Death Rate of\nConfirmed Cases"])

    table_age = LongTable(data_age, colWidths=['50%', '50%'])
    table_age.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1,colors.blue),
                        ('GRID',(0,0),(-1,-1),0.5,colors.blue),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))

    Report.append(Paragraph('Fig.1. Age of Coronavirus Deaths:', ordinary))
    Report.append(Spacer(1, 10))
    Report.append(table_age)
    Report.append(Spacer(1, 12))

    data_sex = [[Paragraph(cell, styleN) for cell in row] for row in data['demographics']['death_rate_by_sex']]
    data_sex.insert(0, ["Sex", "Death Rate of\nConfirmed Cases", "Death Rate of\nAll Cases"])
    (data_sex)

    table_sex = LongTable(data_sex, colWidths=['33%', '33%', '33%'])
    table_sex.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1,colors.blue),
                        ('GRID',(0,0),(-1,-1),0.5,colors.blue),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))

    Report.append(Paragraph('Fig.2. Sex of Coronavirus Deaths:', ordinary))
    Report.append(Spacer(1, 10))
    Report.append(table_sex)
    Report.append(Spacer(1, 12))

    data_disease = [[Paragraph(cell, styleN) for cell in row] for row in data['demographics']['pre_existing_conditions']]
    data_disease.insert(0, ["Pre-Existing\nCondition", "Death Rate of\nConfirmed Cases", "Death Rate of\nAll Cases"])

    table_disease = LongTable(data_age, colWidths=['33%', '33%', '33%'])
    table_disease.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1,colors.blue),
                        ('GRID',(0,0),(-1,-1),0.5,colors.blue),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))

    Report.append(Paragraph('Fig.3. Pre-existing medical conditions (comorbidities):', ordinary))
    Report.append(Spacer(1, 10))
    Report.append(table_disease)
    Report.append(Spacer(1, 12))

    Report.append(PageBreak())

    Report.append(Paragraph('COVID-19 Confirmed Cases and Deaths by Country, Territory, or Conveyance', centered_bold))

    data_proccessed = [[Paragraph(cell, styleN) for cell in row] for row in data['countries']['countries_adv_data']]
    data_proccessed.insert(0, ["Country", "Total\nCases", "New\nCases", "Total\nDeaths", "New\nDeaths", "Total\nRecovered",
                               "Active\nCases", "Serious", "Cases\n1M Pop"])

    table_countries = LongTable(data_proccessed, colWidths=['17%', '10%', '10%', '10%', '10%', '13%', '10%', '10%', '10%'])
    table_countries.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1,colors.blue),
                        ('GRID',(0,0),(-1,-1),0.5,colors.blue),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
    Report.append(table_countries)
    Report.append(Spacer(1, 12))

    Report.append(PageBreak())

    doc = SimpleDocTemplate(url)
    doc.multiBuild(Report, canvasmaker=PageNumCanvas)

    return url