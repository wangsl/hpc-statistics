#!/bin/env python

from xlwt import Workbook, Font, easyxf
from excel import *
from string import replace
from datetime import date
from utility import list_uniq

from chargerate import home_charge_rate, replication_charge_rate, \
     free_home_space, scratch_charge_rate, \
     cpu_time_charge_per_hour, \
     consultation_charge_per_hour, \
     troubleshooting_charge_per_hour 

billing_period_0 = date(2013, 07, 01).strftime('%b %d')
billing_period_1 = date(2013, 07, 31).strftime('%b %d')
billing_period = billing_period_0 + ' - ' + billing_period_1

invoice_date = date.today().strftime('%d-%b-%Y')
invoice_number = 'HPC-' + date.today().strftime('%y%m%d')

def create_invoice_for_pi_2(pi, pi_index, sge_users, disk_users) :

    excel_file = replace(pi.name, ' ', '') + '.xls'
    print " Excel file: ", excel_file

    book = Workbook()
    sheet = book.add_sheet(pi.name)
    sheet.header_str = ""
    sheet.footer_str = ""
    sheet.set_paper_size_code(1)
    sheet.preview_magn = 150
    sheet.page_preview = True

    i = 0
    style = myeasyxf2(colour=1, borders='tttt', font='bold_blue')
    sheet.write_merge(r1=i, c1=0, r2=i, c2=5, style=style,
                      label="High Performance Computing Facility - HPC Core")
    
    i += 2
    style = myeasyxf2(colour=1, borders='tntt', font='bold_black')
    sheet.write_merge(r1=i, c1=0, r2=i, c2=5, style=style,
                      label="Albert Einstein College of Medicine of Yeshiva University")

    i += 1
    style = myeasyxf2(colour=1, borders='nntt', font='black')
    sheet.write_merge(r1=i, c1=0, r2=i, c2=5, style=style,
                      label="Price Center Research Block Pavilion, Room 401")
    i += 1
    sheet.write_merge(r1=i, c1=0, r2=i, c2=5, style=style,
                      label="1301 Morris Park Avenue")
    i += 1
    style = myeasyxf2(colour=1, borders='nttt', font='black')
    sheet.write_merge(r1=i, c1=0, r2=i, c2=5, style=style, label="Bronx, NY 10461")
    
    i += 2
    style = myeasyxf2(font='bold_black')
    sheet.write_merge(r1=i, c1=0, r2=i, c2=5, style=style, label="Dr. John Greally, Facility Supervisor")
    sheet.write_merge(r1=i+2, c1=0, r2=i+2, c2=5, style=style, label="Joseph Hargitai, Facility Director")
    sheet.write_merge(r1=i+4, c1=0, r2=i+4, c2=5, style=style, label="Svetlana Maslova, Facility Administrator")
    
    style = myeasyxf2(font='black')
    sheet.write_merge(r1=i+1, c1=0, r2=i+1, c2=5, style=style, label="718-678-1234; email: john.greally@einstein.yu.edu")
    sheet.write_merge(r1=i+3, c1=0, r2=i+3, c2=5, style=style, label="718-839-7220; email: joseph.hargitai@einstein.yu.edu")
    sheet.write_merge(r1=i+5, c1=0, r2=i+5, c2=5, style=style, label="718-678-1156; email: svetlana.maslova@einstein.yu.edu")
    
    i += 7
    style = myeasyxf2(font='bold_black_underline')
    sheet.write(i, 0, style=style, label="Charge Information")

    i += 2
    style = myeasyxf2(font='bold_black')
    sheet.write(i, 0, style=style, label="User:")
    sheet.write(i+1, 0, style=style, label="Department:")
    sheet.write(i+2, 0, style=style, label="PI/Grant #:")
    sheet.write(i+3, 0, style=style, label="Billing Period:")
    sheet.write(i+4, 0, style=style, label="Invoice Date:")
    sheet.write(i+5, 0, style=style, label="Invoice #:")
    sheet.write(i+6, 0, style=style, label="Charge to account:")

    style = myeasyxf2(alignment='right')
    sheet.write(i, 2, style=style, label=pi.name)

    department = ''
    if pi.department : department = pi.department
    sheet.write(i+1, 2, style=style, label=department)

    grant = '******'
    if pi.grant : grant = pi.grant
    sheet.write(i+2, 2, style=style, label=grant)

    sheet.write(i+3, 2, style=style, label=billing_period)
    sheet.write(i+4, 2, style=style, label=invoice_date)

    invoice = invoice_number + '-' + ('00' + str(pi_index))[-3:]
    
    sheet.write(i+5, 2, style=style, label=invoice)
    sheet.write(i+6, 2, style=style, label="No")

    i += 8

    i_save = i

    i += 10

    style = myeasyxf2(font='bold_black_underline', alignment='left')
    sheet.write(i, 0, style=style, label="Detailed Usage")

    i += 2
    style = myeasyxf2(colour=0, borders='tttt', alignment='center')
    #sheet.write(i, 2, style=style, label='Home usage')
    sheet.write_merge(r1=i, c1=2, r2=i, c2=4, style=style, label='Scratch usage')
    
    i += 1
    style = myeasyxf2(colour=1, borders='tdtn', alignment='right')
    sheet.write(i, 0, style=style, label='Name')
    sheet.write(i, 1, style=style, label='CPU time/Hours')
    #sheet.write(i, 2, style=style, label='home/GB')
    sheet.write(i, 2, style=style, label='cork/GB')
    sheet.write(i, 3, style=style, label='rio/GB')
    style = myeasyxf2(colour=1, borders='tdtt', alignment='right')
    sheet.write(i, 4, style=style, label='oxford/GB')

    hpc_members = list_uniq(pi.sge_members + pi.disk_members)
    n_members = len(hpc_members)

    total_cpu = 0
    
    home_usage = 0
    home_charge = 0
    
    replication_usage = 0
    replication_charge = 0
    
    scratch_usage = 0
    scratch_charge = 0
        
    
    i_mem = 0
    for hpc_mem in hpc_members :
        i += 1
        i_mem += 1
        sge_user = None
        disk_user = None
        name = None

        if sge_users.has_key(hpc_mem) :
            sge_user = sge_users[hpc_mem]
            name = sge_user.name
                        
        if disk_users.has_key(hpc_mem) :
            disk_user = disk_users[hpc_mem]
            name = disk_user.name

        if i_mem == n_members :
            style = myeasyxf2(colour=(i_mem+1)%2, borders='nttn', alignment='right')
        else :
            style = myeasyxf2(colour=(i_mem+1)%2, borders='nntn', alignment='right')

        sheet.write(i, 0, style=style, label=name)

        if sge_user :
            sheet.write(i, 1, float("%.2f" % (sge_user.cpu/3600)), style)
            total_cpu += sge_user.cpu/3600
        else :
            sheet.write(i, 1, None, style)

        if disk_user :
            if disk_user.home :
                #sheet.write(i, 2, float("%.2f" % (disk_user.home)), style)

                home_usage += disk_user.home
                if disk_user.home > free_home_space :
                    home_charge += (disk_user.home - free_home_space)*home_charge_rate
                
                replication_usage += disk_user.home
                if disk_user.home > free_home_space :
                    replication_charge += (disk_user.home - free_home_space)*replication_charge_rate
                
            #else :
            #    sheet.write(i, 2, None, style)
                
            if disk_user.cork :
                sheet.write(i, 2, float("%.2f" % (disk_user.cork)), style)
                scratch_usage += disk_user.cork
                scratch_charge += disk_user.cork*scratch_charge_rate
            else :
                sheet.write(i, 2, None, style)

            if disk_user.rio :
                sheet.write(i, 3, float("%.2f" % (disk_user.rio)), style)
                scratch_usage += disk_user.rio
                scratch_charge += disk_user.rio*scratch_charge_rate
            else :
                sheet.write(i, 3, None, style)

            if i_mem == n_members :
                style = myeasyxf2(colour=(i_mem+1)%2, borders='nttt', alignment='right')
            else :
                style = myeasyxf2(colour=(i_mem+1)%2, borders='nntt', alignment='right')
                
            if disk_user.oxford :
                sheet.write(i, 4, float("%.2f" % (disk_user.oxford)), style)
                scratch_usage += disk_user.oxford
                scratch_charge += disk_user.oxford*scratch_charge_rate
            else :
                sheet.write(i, 4, None, style)
        else :
            #sheet.write(i, 2, None, style)
            sheet.write(i, 2, None, style)
            sheet.write(i, 3, None, style)
            if i_mem == n_members :
                style = myeasyxf2(colour=(i_mem+1)%2, borders='nttt', alignment='right')
            else :
                style = myeasyxf2(colour=(i_mem+1)%2, borders='nntt', alignment='right')
            sheet.write(i, 4, None, style)

    i += 1
    style = myeasyxf2(font='bold_black')
    sheet.write(i, 0, 'Totals:', style)

    style = myeasyxf2(font='bold_black_underline', alignment='right')
    #sheet.write(i, 2, float('%.2f' % home_usage), style)
    sheet.write(i, 1, float('%.2f' % total_cpu), style)
    sheet.write(i, 4, float('%.2f' % scratch_usage), style)

    i += 2
    sheet.write_merge(r1=i, c1=0, r2=i, c2=5, label='If there are any inquiries regarding your billing invoice,')
    i += 1
    sheet.write_merge(r1=i, c1=0, r2=i, c2=5, label='please do not hesitate to contact the facility administrator.')
            
    
    i = i_save

    style = myeasyxf2(colour=1, borders='tntt', alignment='right')
    sheet.write(i, 0, "Period", style)
    sheet.write(i, 1, "Description", style)
    sheet.write(i, 2, "Number of Hours", style)
    sheet.write(i, 3, "Cost per Hour", style)
    sheet.write(i, 4, "Price", style)

    i += 1
    style = myeasyxf2(colour = 0, borders='tntt', alignment='right')
    sheet.write(i, 0, billing_period, style)
    sheet.write(i, 1, "CPU usage", style)
    sheet.write(i, 2, float("%.2f" % total_cpu), style)

    sheet.write(i+1, 0, billing_period, style)
    sheet.write(i+1, 1, "Consultation", style)
    sheet.write(i+1, 2, float("%.2f" % pi.consultation), style)

    style = myeasyxf2(colour = 0, borders='tttt', alignment='right')
    sheet.write(i+2, 0, billing_period, style)
    sheet.write(i+2, 1, "Troubleshooting", style)
    sheet.write(i+2, 2, float("%.2f" % pi.troubleshooting), style)

    style = myeasyxf2(colour = 0, borders='tntt', alignment='right', num_format_str='$#0.00')
    sheet.write(i, 3, float('%.2f' % cpu_time_charge_per_hour), style)
    sheet.write(i, 4, float('%.2f' % (total_cpu*cpu_time_charge_per_hour)), style)

    sheet.write(i+1, 3, float('%.2f' % consultation_charge_per_hour), style)
    sheet.write(i+1, 4, float('%.2f' % (pi.consultation*consultation_charge_per_hour)), style)

    style = myeasyxf2(colour = 0, borders='tttt', alignment='right', num_format_str='$#0.00')
    sheet.write(i+2, 3, float('%.2f' % troubleshooting_charge_per_hour), style)
    sheet.write(i+2, 4, float('%.2f' % (troubleshooting_charge_per_hour*pi.troubleshooting)), style)
    
    i += 4
    style = myeasyxf2(colour=1, borders='tntt', alignment='right')
    sheet.write(i, 0, "Period", style)
    sheet.write(i, 1, "Description", style)
    sheet.write(i, 2, "Data GB", style)
    sheet.write(i, 3, "Cost per GB", style)
    sheet.write(i, 4, "Price", style)

    style = myeasyxf2(colour = 0, borders='tttt', alignment='right')
    #sheet.write(i+1, 0, billing_period, style)
    #sheet.write(i+1, 1, "Home usage", style)
    #sheet.write(i+1, 2, float('%.2f' % home_usage), style)

    sheet.write(i+1, 0, billing_period, style)
    sheet.write(i+1, 1, "Scratch usage", style)
    sheet.write(i+1, 2, float('%.2f' % scratch_usage), style)

    #replication_usage += pi.shares_replication
    #sheet.write(i+3, 0, billing_period, style)
    #sheet.write(i+3, 1, "Replication usage", style)
    #sheet.write(i+3, 2, float('%.2f' % replication_usage), style)

    #sheet.write(i+4, 0, billing_period, style)
    #sheet.write(i+4, 1, "Shares usage", style)
    #sheet.write(i+4, 2, float('%.2f' % pi.shares), style)

    #style = myeasyxf2(colour = 0, borders='tntt', alignment='right', num_format_str='$#0.0000')
    #sheet.write(i+1, 3, float('%.4f' % (home_charge_rate)), style)
    sheet.write(i+1, 3, float('%.4f' % (scratch_charge_rate)), style)

    #style = myeasyxf2(colour = 0, borders='tntt', alignment='right', num_format_str='$#0.00')
    #sheet.write(i+1, 4, float('%.2f' % home_charge), style)
    sheet.write(i+1, 4, float('%.2f' % scratch_charge), style)

    #replication_charge += pi.shares_replication*replication_charge_rate
    #style = myeasyxf2(colour = 0, borders='tttt', alignment='right', num_format_str='$#0.0000')
    #sheet.write(i+3, 3, float('%.4f' % (replication_charge_rate)), style)

    #style = myeasyxf2(colour = 0, borders='tttt', alignment='right', num_format_str='$#0.00')
    #sheet.write(i+3, 4, float('%.2f' % replication_charge), style)

    #style = myeasyxf2(colour = 0, borders='tttt', alignment='right', num_format_str='$#0.0000')
    #sheet.write(i+4, 3, float('%.4f' % (home_charge_rate)), style)

    #style = myeasyxf2(colour = 0, borders='tttt', alignment='right', num_format_str='$#0.00')
    #sheet.write(i+4, 4, float('%.2f' % (pi.shares*home_charge_rate)), style)

    i += 3

    style = myeasyxf2(colour = 0, alignment='right', font = 'bold_black_underline')
    sheet.write(i, 3, 'Total cost:', style)

    total_charge = total_cpu*cpu_time_charge_per_hour + \
                   pi.consultation*consultation_charge_per_hour + \
                   pi.troubleshooting*troubleshooting_charge_per_hour + \
                   scratch_charge 

    style = myeasyxf2(colour = 0, alignment='right', font = 'bold_black_underline',
                      num_format_str='$#0.00')
    sheet.write(i, 4, float('%.2f' % total_charge), style)
                
    book.save(excel_file)
    
    return total_charge

