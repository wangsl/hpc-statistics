#!/bin/env python

from glob import glob
from utility import check_file_exists, is_blank_line
from excel import *
from xlwt import Workbook
from chargerate import *

usages = None

class SharedPI :

    def __init__(self) :
        self.name = None
        self.owner = None
        self.shared_files = {}
        return

    def total_usage(self) :
        total_size = 0
        total_replication = 0
        for k in self.shared_files.keys() :
            total_size += self.shared_files[k][0]
            total_replication += self.shared_files[k][1]
        return [ total_size, total_replication ]

def setup_usages() :
    global usages
    
    usages = {}

    shared_files = glob('shares/[a-z]*')

    for f in shared_files :
        check_file_exists(f)
        tmp = f.split('/')
        assert len(tmp) == 2
        shared_file = tmp[1]

        fin = open(f, "r")
        assert fin
        while 1 :
            line = fin.readline()
            if not line : break
            if is_blank_line(line) : continue
            line = line.strip()
            tmp = line.split(':')
            if len(tmp) != 4 :
                print len(tmp)
                print line
            assert len(tmp) == 4
            owner = tmp[0].strip().lstrip()
            name = tmp[1].strip().lstrip()
            size = float(tmp[2])
            replication = 0
            if len(tmp) == 4 :
                replication = float(tmp[3])

            if not usages.has_key(owner) :
                shared_pi = SharedPI()
                shared_pi.name = name
                shared_pi.owner = owner
                usages[owner] = shared_pi 
                
            usages[owner].shared_files[shared_file] = [ size, replication ]
            
        fin.close()

def print_usages() :
    global usages

    for u in usages.keys() :
        total = usages[u].total_usage()
        print u, total[0], total[1]

def write_to_excel(excel_file = 'shared-usage.xls') :

    book = Workbook()
    sheet = book.add_sheet('shared usage')
    sheet.portrait = False
    sheet.set_paper_size_code(1)

    i = 0
    style = myeasyxf(colour = (i+1)%2, borders='mdmn')
    sheet.write(i, 0, "PI", style)
    
    style = myeasyxf(colour = (i+1)%2, borders='mdtn')
    sheet.write(i, 1, "ID", style)
    sheet.write(i, 2, "Grant Number", style)
    sheet.write(i, 3, "Disk (GB)", style)
    sheet.write(i, 4, "Replication (GB)", style)
    sheet.write(i, 5, "Charge", style)
    sheet.write(i, 6, "File", style)
    sheet.write(i, 7, "Disk (GB)", style)
    sheet.write(i, 8, "Replication (GB)", style)
    style = myeasyxf(colour = (i+1)%2, borders='mdtm')
    sheet.write(i, 9, "Charge", style)
    i +=1

    total_disk_usage = 0
    total_replication_usage = 0
    total_charge = 0

    for pi in usages.keys() :
        n_files = len(usages[pi].shared_files.keys())
        total_usage = usages[pi].total_usage()
        total_disk_usage += total_usage[0]
        total_replication_usage += total_usage[1]

        charge = (total_usage[0] + total_usage[1]) *charge_rate
        total_charge += charge
        
        style = myeasyxf(colour = 0, borders='ntmn')
        sheet.write_merge(r1=i, c1=0, r2=i+n_files-1, c2=0,
                          label=usages[pi].name, style=style)

        style = myeasyxf(colour = 0, borders='nttn')
        sheet.write_merge(r1=i, c1=1, r2=i+n_files-1, c2=1,
                          label=usages[pi].owner, style=style)

        sheet.write_merge(r1=i, c1=2, r2=i+n_files-1, c2=2,
                          label=None, style=style)

        sheet.write_merge(r1=i, c1=3, r2=i+n_files-1, c2=3,
                          label=float("%.2f" % (total_usage[0])), style=style)

        sheet.write_merge(r1=i, c1=4, r2=i+n_files-1, c2=4,
                          label=float("%.2f" % (total_usage[1])), style=style)

        sheet.write_merge(r1=i, c1=5, r2=i+n_files-1, c2=5,
                          label=float("%.2f" % (charge)), style=style)

        i_file = 0
        for f in usages[pi].shared_files.keys() :
            i_file += 1
            charge = (usages[pi].shared_files[f][0] + usages[pi].shared_files[f][1]) * charge_rate
            style = myeasyxf(colour = (i+1)%2, borders='nntn')
            if i_file == n_files :
                style = myeasyxf(colour = (i+1)%2, borders='nttn')
            sheet.write(i, 6, f, style)
            sheet.write(i, 7, float("%.2f" % (usages[pi].shared_files[f][0])), style)
            sheet.write(i, 8, float("%.2f" % (usages[pi].shared_files[f][1])), style)

            style = myeasyxf(colour = (i+1)%2, borders='nntm')
            if i_file == n_files :
                style = myeasyxf(colour = (i+1)%2, borders='nttm')
            sheet.write(i, 9, float("%.2f" % (charge)), style)
            
            i += 1

    style = myeasyxf(colour = (i+1)%2, borders='dmmn')
    sheet.write(i, 0, "Total", style)

    style = myeasyxf(colour = (i+1)%2, borders='dmtn')
    sheet.write(i, 1, None, style)
    sheet.write(i, 2, None, style)
    sheet.write(i, 3, float("%.2f" % (total_disk_usage)), style)
    sheet.write(i, 4, float("%.2f" % (total_replication_usage)), style)
    sheet.write(i, 5, float("%.2f" % (total_charge)), style)
    sheet.write(i, 6, None, style)
    sheet.write(i, 7, float("%.2f" % (total_disk_usage)), style)
    sheet.write(i, 8, float("%.2f" % (total_replication_usage)), style)
    style = myeasyxf(colour = (i+1)%2, borders='dmtm')
    sheet.write(i, 9, float("%.2f" % (total_charge)), style)
    
    book.save(excel_file)
    return
    
if __name__ == "__main__" :

    setup_usages()
    print_usages()
    
    write_to_excel()
    

    


