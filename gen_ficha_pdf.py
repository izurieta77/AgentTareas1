# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUT = "/home/user/AgentTareas1/ficha-tecnica-shutters-asturvent.pdf"
BLACK = colors.HexColor("#0b0b0b"); HEAD = colors.HexColor("#0b3b5c")
GREY = colors.HexColor("#f3f3f3"); LINE = colors.HexColor("#cccccc")
styles = getSampleStyleSheet()
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, textColor=BLACK, spaceAfter=1, alignment=TA_CENTER)
sub = ParagraphStyle("sub", fontSize=8, textColor=colors.grey, alignment=TA_CENTER, spaceAfter=6)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10, textColor=HEAD, spaceBefore=7, spaceAfter=3)
nm = ParagraphStyle("nm", fontSize=8, leading=10)
small = ParagraphStyle("small", fontSize=7, textColor=colors.grey, leading=9)

doc = SimpleDocTemplate(OUT, pagesize=LETTER, topMargin=12*mm, bottomMargin=10*mm, leftMargin=15*mm, rightMargin=15*mm,
                        title="Ficha tecnica de shutters - Asturvent", author="Eduardo Izurieta - Asturvent")
S = []
hdr = Table([[Paragraph('<font color="white"><b>ASTURVENT</b></font>', ParagraphStyle("w", fontSize=13, alignment=TA_LEFT)),
             Paragraph('<font color="white">Puertas y Ventanas de Asturias, S.A. de C.V.<br/>Silencio &middot; Confort &middot; K&ouml;mmerling</font>', ParagraphStyle("w2", fontSize=7.5, alignment=2, leading=10))]],
            colWidths=[60*mm, 120*mm])
hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),BLACK),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                         ("LEFTPADDING",(0,0),(-1,-1),9),("RIGHTPADDING",(0,0),(-1,-1),9),
                         ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
S.append(hdr); S.append(Spacer(1,6))
S.append(Paragraph("Ficha t&eacute;cnica de shutters para cotizaci&oacute;n", h1))
S.append(Paragraph("19 persianas / shutters enrollables de lama r&iacute;gida de aluminio o PVC &mdash; medidas en metros (ancho &times; alto)", sub))

def tbl(data, colw, header=True):
    t = Table(data, colWidths=colw)
    st = [("GRID",(0,0),(-1,-1),0.5,LINE),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("FONTSIZE",(0,0),(-1,-1),7.8),
          ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),("TOPPADDING",(0,0),(-1,-1),2.5),("BOTTOMPADDING",(0,0),(-1,-1),2.5)]
    if header: st += [("BACKGROUND",(0,0),(-1,0),GREY),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")]
    t.setStyle(TableStyle(st)); return t

S.append(Paragraph("1. Resumen de piezas", h2))
piezas = [["Pos.","Identificador","Medida (ancho x alto)","Operación","Preparación","Pzas"],
          ["1","SHU 01 / Shutter 1","1.56 x 3.00 m","Motorizada por botonera","Lado izquierdo","6"],
          ["2","SHU 02 / Shutter 2","0.60 x 0.60 m","Manual","Lado izquierdo","2"],
          ["3","SHU 03 / Shutter 3","1.20 x 0.60 m","Motorizada por botonera","Lado izquierdo","8"],
          ["4","SHU 04 / Shutter 4","2.20 x 1.50 m","Motorizada por botonera","Lado izquierdo","3"],
          ["","","","","Total","19"]]
t = tbl(piezas,[11*mm,36*mm,37*mm,40*mm,28*mm,13*mm])
t.setStyle(TableStyle([("BACKGROUND",(0,5),(-1,5),GREY),("FONTNAME",(4,5),(-1,5),"Helvetica-Bold"),("SPAN",(0,5),(3,5))]))
S.append(t)
S.append(Paragraph("2. Especificaciones comunes (producto)", h2))
S.append(tbl([["Lama","Privacidad C-45 (lama rígida; NO cortina de tela)"],
        ["Material / relleno","Aluminio rolado con espuma de poliuretano, o equivalente en PVC"],
        ["Color","Blanco"],["Cajón","Blanco (PVC o aluminio)"],["Guía","Aluminio color blanco"],
        ["Preparación","Lado izquierdo en las cuatro posiciones"]],[42*mm,123*mm],header=False))
S.append(Paragraph("3. Accionamiento", h2))
S.append(tbl([["Pos. 1, 3 y 4","Motorizado, operado por BOTONERA (interruptor de pared). No requiere control remoto."],
       ["Pos. 2","Operación manual (cinta o manivela)"],
       ["Motor","Tubular para persiana enrollable, 127 Vca / 60 Hz"],
       ["Sensor de obstáculos","Deseable (indicar si lo incluye)"],["Flejes de seguridad","Sí"]],[42*mm,123*mm],header=False))
S.append(Paragraph("4. Datos técnicos de referencia (lama de aluminio C-45)", h2))
S.append(tbl([["Material","Aluminio 3105 H46"],["Superficie de cobertura","45 mm"],["Espesor nominal","9 mm"],
       ["Espesor banda total","0.285 ± 0.02 mm"],["Lamas por metro de altura","22"],["Eje mínimo de enrollamiento","Ø 40"],
       ["Peso por m²","D90 2.610 kg / D125 2.820 kg"],["Clasificación fuego","M1 (NF P 92-507:2004), informe 8530 AITEX"],
       ["Resistencia térmica adicional","EN 13125:2001 — Clase 4: 0.15 m²K/W; Clase 5: 0.18 m²K/W"]],[52*mm,113*mm],header=False))
S.append(Spacer(1,5))
S.append(Paragraph("<b>Nota:</b> se solicita precio unitario y total por posición, subtotal/IVA/total, en dos modalidades "
                   "(a) solo fabricación y suministro y (b) suministro con instalación en CDMX / Zona Metropolitana, "
                   "indicando tiempo de entrega, garantía y vigencia.", nm))
S.append(Spacer(1,7))
S.append(Paragraph("Eduardo Izurieta &mdash; Asistente del CEO &middot; Puertas y Ventanas de Asturias, S.A. de C.V. (Asturvent) &middot; "
                   "Cel. 55 4797 7723 &middot; izurieta77@gmail.com &middot; asturvent-web.netlify.app", small))
doc.build(S)
import os
print("PDF OK bytes:", os.path.getsize(OUT))
