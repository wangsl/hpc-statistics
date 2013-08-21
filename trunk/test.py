#!/bin/env python

from xlwt import Workbook, Font, easyxf
from excel import *

book = Workbook()

sheet = book.add_sheet('HPC usage')
#sheet.portrait = False
sheet.header_str = "" #HPC invoice"
sheet.footer_str = "" #None #"HPC invoic222"
sheet.set_paper_size_code(1)

sheet.page_preview = True

i = 0
style = myeasyxf2(colour=1, borders='tttt', font='bold_blue', alignment='left')
sheet.write_merge(r1=i, c1=0, r2=i, c2=4, style=style,
                  label="High Performance Computing Facility - HPC Core")

i += 2
style = myeasyxf2(colour=1, borders='tntt', font='bold_black', alignment='left')
sheet.write_merge(r1=i, c1=0, r2=i, c2=4, style=style,
                  label="Albert Einstein College of Medicine of Yeshiva University")

i += 1
style = myeasyxf2(colour=1, borders='nntt', font='black', alignment='left')
sheet.write_merge(r1=i, c1=0, r2=i, c2=4, style=style,
                  label="Price Center Research Block Pavilion, Room 401")
i += 1
sheet.write_merge(r1=i, c1=0, r2=i, c2=4, style=style,
                  label="1301 Morris Park Avenue")
i += 1
style = myeasyxf2(colour=1, borders='nttt', font='black', alignment='left')
sheet.write_merge(r1=i, c1=0, r2=i, c2=4, style=style, label="Bronx, NY 10461")

i += 2
style = myeasyxf2(font='bold_black', alignment='left')
sheet.write_merge(r1=i, c1=0, r2=i, c2=4, style=style, label="Dr. John Greally, Facility Supervisor")
sheet.write_merge(r1=i+2, c1=0, r2=i+2, c2=4, style=style, label="Joseph Hargitai, Facility Director")
sheet.write_merge(r1=i+4, c1=0, r2=i+4, c2=4, style=style, label="Svetlana Maslova, Facility Administrator")

style = myeasyxf2(font='black', alignment='left')
sheet.write_merge(r1=i+1, c1=0, r2=i+1, c2=4, style=style, label="718-678-1234; email: john.greally@einstein.yu.edu")
sheet.write_merge(r1=i+3, c1=0, r2=i+3, c2=4, style=style, label="718-839-7220; email: joseph.hargitai@einstein.yu.edu")
sheet.write_merge(r1=i+5, c1=0, r2=i+5, c2=4, style=style, label="718-678-1156; email: svetlana.maslova@einstein.yu.edu")

i += 7
style = myeasyxf2(font='bold_black_underline', alignment='left')
sheet.write(i, 0, style=style, label="Charge Information")

i += 1
style = myeasyxf2(font='bold_black', alignment='left')
sheet.write(i, 0, style=style, label="User:")
sheet.write(i+1, 0, style=style, label="Department")
sheet.write(i+2, 0, style=style, label="PI/Grant #:")
sheet.write(i+3, 0, style=style, label="Billing Period:")
sheet.write(i+4, 0, style=style, label="Invoice Date:")
sheet.write(i+5, 0, style=style, label="Invoice #:")
sheet.write(i+6, 0, style=style, label="Charge to account:")

style = myeasyxf2(alignment='right')
sheet.write(i, 2, style=style, label="PI Name")
sheet.write(i+1, 2, style=style, label="Unknown")
sheet.write(i+2, 2, style=style, label="******")
sheet.write(i+3, 2, style=style, label="July 2013")
sheet.write(i+4, 2, style=style, label="12-Aug-2013")
sheet.write(i+5, 2, style=style, label="XXX-XX")
sheet.write(i+6, 2, style=style, label="No")

i += 7

i += 2
style = myeasyxf2(colour=1, borders='tntt', font='bold_black', alignment='right')
sheet.write(i, 0, "Period", style)
sheet.write(i, 1, "Description", style)
sheet.write(i, 2, "Number of Hours", style)
sheet.write(i, 3, "Cost per Hour", style)
sheet.write(i, 4, "Price", style)

i += 1
style = myeasyxf2(colour = 0, borders='tntt', alignment='right')
sheet.write(i, 0, "Jul-2013", style)
sheet.write(i, 1, "CPU usage", style)
sheet.write(i, 2, 876.0, style)

sheet.write(i+1, 0, "Jul-2013", style)
sheet.write(i+1, 1, "Consultation", style)
sheet.write(i+1, 2, 0.0, style)

style = myeasyxf2(colour = 0, borders='tntt', alignment='right', num_format_str='$#0.00')
sheet.write(i, 3, 0.05, style)
sheet.write(i, 4, 43.80, style)

sheet.write(i+1, 3, 65.0, style)
sheet.write(i+1, 4, 0.0, style)

style = myeasyxf2(colour = 0, borders='tttt', alignment='right')

sheet.write(i+2, 0, "Jul-2013", style)
sheet.write(i+2, 1, "Troubleshooting", style)
sheet.write(i+2, 2, 0.0, style)

style = myeasyxf2(colour = 0, borders='tttt', alignment='right', num_format_str='$#0.00')

sheet.write(i+2, 3, 25.0, style)
sheet.write(i+2, 4, 0.0, style)

i += 4

style = myeasyxf2(colour=1, borders='tntt', font='bold_black', alignment='right')
sheet.write(i, 0, "Period", style)
sheet.write(i, 1, "Description", style)
sheet.write(i, 2, "Data GB", style)
sheet.write(i, 3, "Cost per GB", style)
sheet.write(i, 4, "Price", style)

i += 1
style = myeasyxf2(colour = 0, borders='tttt', alignment='right')
sheet.write(i, 0, "Jul-2013", style)
sheet.write(i, 1, "Home usage", style)
sheet.write(i, 2, 0.0, style)

sheet.write(i+1, 0, "Jul-2013", style)
sheet.write(i+1, 1, "Scratch usage", style)
sheet.write(i+1, 2, 0.0, style)

sheet.write(i+2, 0, "Jul-2013", style)
sheet.write(i+2, 1, "Replication usage", style)
sheet.write(i+2, 2, 0.0, style)

style = myeasyxf2(colour = 0, borders='tttt', alignment='right', num_format_str='$#0.00')
sheet.write(i,   3, 65.0, style)
sheet.write(i+1, 3, 35.0, style)
sheet.write(i+2, 3, 35.0, style)

sheet.write(i,   4, 0.0, style)
sheet.write(i+1, 4, 0.0, style)
sheet.write(i+2, 4, 0.0, style)

i += 5
style = myeasyxf2(font='bold_black_underline', alignment='left')
sheet.write(i, 0, style=style, label="Detailed Usage")


#sheet.write(i+2, 0, 0, style)

#sheet.write(i, 3, 64.00, style)
#sheet.write(i, 4, 0.0, style)



book.save("t1.xls")





