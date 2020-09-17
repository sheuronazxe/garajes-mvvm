import hashlib, subprocess
from PyQt5.QtCore import QSortFilterProxyModel
from reportlab.lib.colors import black, gray
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def GenerarPDF(modelo, fecha):
    pdfmetrics.registerFont(TTFont('kau','fuentes\KaushanScript-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('comme','fuentes\Comme-Medium.ttf'))

    pdf = canvas.Canvas('datos/informe.pdf')
    pdf.setTitle('Recibos')
    pdf.setLineWidth(0.5)

    fecha = fecha.date().toString("MMMM yyyy").capitalize()
    ancla = 795
    for index in range(modelo.rowCount()):
        nombre = modelo.index(index,1).data()
        garaje = modelo.index(index,3).data()
        alquiler = modelo.index(index,4).data()

        pdf.setFont('kau', 26)
        pdf.drawString(30, ancla, "Recibo")
        pdf.setStrokeAlpha(0.3)
        pdf.rect(30, ancla-40, 120, 25, stroke=1, fill=0)
        pdf.rect(170, ancla-40, 180, 25, stroke=1, fill=0)
        pdf.rect(495, ancla-40, 70, 25, stroke=1, fill=0)
        pdf.setStrokeAlpha(1)
        pdf.roundRect(30, ancla-135, 535, 80, 6, stroke=1, fill=0)

        pdf.setFont('comme', 10)
        pdf.setFillColor(gray)
        pdf.drawString(40, ancla-79, "NOMBRE")
        pdf.drawString(430, ancla-79, "PLAZA DE GARAJE")
        clave = int(hashlib.sha1((nombre+fecha).encode('UTF-8')).hexdigest(), 16) % (10 ** 8)
        pdf.drawCentredString(90, ancla-32, "ID: " + str(clave))
       
        pdf.setFont('comme', 16)
        pdf.setFillColor(black)
        pdf.drawCentredString(260, ancla-34, fecha)
        pdf.drawCentredString(530, ancla-34, str(alquiler) + " €")
        pdf.drawString(50, ancla-110, nombre)
        pdf.drawString(440, ancla-110, garaje)

        pdf.setDash(1,2)
        pdf.lines([(0, ancla-163.5, 20, ancla-163.5),(575, ancla-163.5, 595, ancla-163.5)])
        pdf.setDash()
        ancla -= 210.5

        if ancla < 0:
            ancla = 795
            pdf.showPage()

    pdf.save()
    subprocess.Popen(f'datos\informe.pdf',shell=True)
    
