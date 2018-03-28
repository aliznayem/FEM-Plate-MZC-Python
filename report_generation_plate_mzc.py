from pylab import *
import time
from reportlab.lib.enums import TA_CENTER, TA_LEFT
# from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import utils

def get_image(path, width=1*inch):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

def report_generation_plate_mzc(length, width, thick, young, poiss, denss, npnod, nelem, uz, xtheta, ytheta, zf, xm, ym,
                                mx, my, mxy, file_name):

    # Find max. values
    uzmax = max(uz, key=abs)
    uzmin = min(uz, key=abs)
    xthetamax = max(xtheta, key=abs)
    xthetamin = min(xtheta, key=abs)
    ythetamax = max(ytheta, key=abs)
    ythetamin = min(ytheta, key=abs)

    mxmax = max(mx, key=abs)
    mxmin = min(mx, key=abs)
    mymax = max(my, key=abs)
    mymin = min(my, key=abs)
    mxymax = max(mxy, key=abs)
    mxymin = min(mxy, key=abs)

    zfmax = max(zf, key=abs)
    zfmin = min(zf, key=abs)
    xmmax = max(xm, key=abs)
    xmmin = min(xm, key=abs)
    ymmax = max(ym, key=abs)
    ymmin = min(ym, key=abs)

    file = file_name + '_report_plate_mzc.pdf'

    doc = SimpleDocTemplate(file,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    Story = []

    heading = "FEM Analysis Report on Rectangular Thin Plate Loading"
    sub_heading = "(Non-conforming 4-noded MZC Rectangular Element)"
    imgfile1 = 'figures/zdisp.png'
    imgfile2 = 'figures/xrot.png'
    imgfile3 = 'figures/yrot.png'
    imgfile4 = 'figures/mx.png'
    imgfile5 = 'figures/my.png'
    imgfile6 = 'figures/mxy.png'
    imgfile7 = 'figures/zf.png'
    imgfile8 = 'figures/xm.png'
    imgfile9 = 'figures/ym.png'

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Heading', alignment=TA_CENTER, fontName='Helvetica-Bold', fontSize=16))
    styles.add(ParagraphStyle(name='SubHeading', alignment=TA_CENTER, fontName='Helvetica-Bold', fontSize=12))
    styles.add(ParagraphStyle(name='SecHeading', alignment=TA_CENTER, fontName='Helvetica', fontSize=12))
    styles.add(ParagraphStyle(name='Simple', alignment=TA_LEFT, fontName='Helvetica', fontSize=10))
    styles.add(ParagraphStyle(name='Footer', alignment=TA_LEFT, fontName='Helvetica', fontSize=8))

    # Heading
    # ptext = '<font size=16>%s</font>' % heading
    Story.append(Paragraph(heading, styles["Heading"]))
    Story.append(Spacer(1, 8))
    # ptext = '<font size=12>%s</font>' % sub_heading
    Story.append(Paragraph(sub_heading, styles["SubHeading"]))
    Story.append(Spacer(1, 40))

    # Plate variables section
    Story.append(Paragraph('Plate Variables', styles["SecHeading"]))
    Story.append(Spacer(1, 15))
    Story.append(Paragraph('Length: {:.2f}'.format(length), styles["Simple"]))
    # Story.append(Spacer(1, 2))
    Story.append(Paragraph('Width: {:.2f}'.format(width), styles["Simple"]))
    # Story.append(Spacer(1, 2))
    Story.append(Paragraph('Thickness: {:.4f}'.format(thick), styles["Simple"]))
    # Story.append(Spacer(1, 2))
    Story.append(Paragraph('Density: {:.2g}'.format(denss), styles["Simple"]))
    # Story.append(Spacer(1, 2))
    Story.append(Paragraph('Young\'s Modulus: {:.2g}'.format(young), styles["Simple"]))
    # Story.append(Spacer(1, 2))
    Story.append(Paragraph('Poisson\'s Ratio: {:.2f}'.format(poiss), styles["Simple"]))
    Story.append(Spacer(1, 20))

    # Reslt summary section
    Story.append(Paragraph('Result Summary', styles["SecHeading"]))
    Story.append(Spacer(1, 15))
    Story.append(Paragraph('Total Nodes: {:.0f}'.format(npnod), styles["Simple"]))
    Story.append(Paragraph('Total Elements: {:.0f}'.format(nelem), styles["Simple"]))
    Story.append(Spacer(1, 8))
    Story.append(Paragraph('Max. Vertical Displacement: {:.5g}'.format(uzmax), styles["Simple"]))
    Story.append(Paragraph('Min. Vertical Displacement: {:.5g}'.format(uzmin), styles["Simple"]))
    Story.append(Paragraph('Max. X-Rotation: {:.5g}'.format(xthetamax), styles["Simple"]))
    Story.append(Paragraph('Min. X-Rotation: {:.5g}'.format(xthetamin), styles["Simple"]))
    Story.append(Paragraph('Max. Y-Rotation: {:.5g}'.format(ythetamax), styles["Simple"]))
    Story.append(Paragraph('Min. Y-Rotation: {:.5g}'.format(ythetamin), styles["Simple"]))
    Story.append(Spacer(1, 8))
    Story.append(Paragraph('Max. Mx-Stress: {:.5g}'.format(mxmax), styles["Simple"]))
    Story.append(Paragraph('Min. Mx-Stress: {:.5g}'.format(mxmin), styles["Simple"]))
    Story.append(Paragraph('Max. My-Stress: {:.5g}'.format(mymax), styles["Simple"]))
    Story.append(Paragraph('Min. My-Stress: {:.5g}'.format(mymin), styles["Simple"]))
    Story.append(Paragraph('Max. Mxy-Stress: {:.5g}'.format(mxymax), styles["Simple"]))
    Story.append(Paragraph('Min. Mxy-Stress: {:.5g}'.format(mxymin), styles["Simple"]))
    Story.append(Spacer(1, 8))
    Story.append(Paragraph('Max. Vertical Reaction Force: {:.5g}'.format(zfmax), styles["Simple"]))
    Story.append(Paragraph('Min. Vertical Reaction Force: {:.5g}'.format(zfmin), styles["Simple"]))
    Story.append(Paragraph('Max. X-Reaction Moment: {:.5g}'.format(xmmax), styles["Simple"]))
    Story.append(Paragraph('Min. X-Reaction Moment: {:.5g}'.format(xmmin), styles["Simple"]))
    Story.append(Paragraph('Max. Y-Reaction Moment: {:.5g}'.format(ymmax), styles["Simple"]))
    Story.append(Paragraph('Min. Y-Reaction Moment: {:.5g}'.format(ymmin), styles["Simple"]))
    # Story.append(Spacer(1, 20))

    Story.append(PageBreak())

    # Contour plots
    Story.append(Paragraph('Contour Plots', styles["SecHeading"]))
    Story.append(Spacer(1, 15))

    Story.append(get_image(imgfile1, width=4*inch))
    Story.append(get_image(imgfile2, width=4*inch))
    Story.append(get_image(imgfile3, width=4*inch))
    Story.append(get_image(imgfile4, width=4*inch))
    Story.append(get_image(imgfile5, width=4*inch))
    Story.append(get_image(imgfile6, width=4*inch))
    Story.append(get_image(imgfile7, width=4 * inch))
    Story.append(get_image(imgfile8, width=4 * inch))
    Story.append(get_image(imgfile9, width=4 * inch))

    Story.append(Paragraph(time.ctime(), styles["Footer"]))

    doc.build(Story)

    print("Report generated")