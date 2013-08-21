#!/bin/env python

from glob import glob
from utility import check_file_exists
from excel import *
from xlwt import Workbook
from chargerate import *

usages = None

class PI :

    def __init__(self) :
        self.name = None
        self.owner = None
        self.servers = {}
        return

    def total_usage(self) :
        total = 0
        for k in self.servers.keys() :
            total += self.servers[k]
        return total

def setup_usages(input_file) :
    global usages
    usages = {}
    
    check_file_exists(input_file)

    print " Raeding from file: " + input_file

    fin = open(input_file, "r")
    assert fin
    while 1 :
        line = fin.readline()
        if not line : break
        line = line.strip()
        tmp = line.split(':')
        if len(tmp) != 4 :
            print line
            print len(tmp)
        assert len(tmp) >= 4
        server = tmp[0].strip().lstrip()
        name = tmp[1].strip().lstrip()
        owner = tmp[2].strip().lstrip()
        size = float(tmp[3])

        if not usages.has_key(name) :
            pi = PI()
            pi.name = name
            pi.owner = owner
            usages[name] = pi 
                
        usages[name].servers[server] = size
            
    fin.close()

def print_usages() :
    global usages

    for u in usages.keys() :
        print u, usages[u].total_usage()

def write_to_excel(excel_file, sheet) :

    book = Workbook()
    sheet = book.add_sheet(sheet)
    sheet.portrait = False
    sheet.set_paper_size_code(1)

    i = 0
    style = myeasyxf(colour = (i+1)%2, borders='mdmn')
    sheet.write(i, 0, "PI", style)
    
    style = myeasyxf(colour = (i+1)%2, borders='mdtn')
    sheet.write(i, 1, "ID", style)
    sheet.write(i, 2, "Grant Number", style)
    sheet.write(i, 3, "Sys-Admin", style)
    sheet.write(i, 4, "Server", style)

    style = myeasyxf(colour = (i+1)%2, borders='mdtm')
    sheet.write(i, 5, "Sys-Admin", style)
    i +=1

    total_disk_usage = 0

    for pi in usages.keys() :
        n_files = len(usages[pi].servers.keys())
        total_usage = usages[pi].total_usage()
        total_disk_usage += total_usage
        
        style = myeasyxf(colour = 0, borders='ntmn')
        sheet.write_merge(r1=i, c1=0, r2=i+n_files-1, c2=0,
                          label=usages[pi].name, style=style)

        style = myeasyxf(colour = 0, borders='nttn')
        sheet.write_merge(r1=i, c1=1, r2=i+n_files-1, c2=1,
                          label=usages[pi].owner, style=style)

        sheet.write_merge(r1=i, c1=2, r2=i+n_files-1, c2=2,
                          label=None, style=style)

        sheet.write_merge(r1=i, c1=3, r2=i+n_files-1, c2=3,
                          label=float("%.2f" % (total_usage)), style=style)

        i_file = 0
        for f in usages[pi].servers.keys() :
            i_file += 1
            style = myeasyxf(colour = (i+1)%2, borders='nntn')
            if i_file == n_files :
                style = myeasyxf(colour = (i+1)%2, borders='nttn')
            sheet.write(i, 4, f, style)

            style = myeasyxf(colour = (i+1)%2, borders='nntm')
            if i_file == n_files :
                style = myeasyxf(colour = (i+1)%2, borders='nttm')
            sheet.write(i, 5, float("%.2f" % (usages[pi].servers[f])), style)
            
            i += 1

    style = myeasyxf(colour = (i+1)%2, borders='dmmn')
    sheet.write(i, 0, "Total", style)

    style = myeasyxf(colour = (i+1)%2, borders='dmtn')
    sheet.write(i, 1, None, style)
    sheet.write(i, 2, None, style)
    sheet.write(i, 3, float("%.2f" % (total_disk_usage)), style)
    sheet.write(i, 4, None, style)
    style = myeasyxf(colour = (i+1)%2, borders='dmtm')
    sheet.write(i, 5, float("%.2f" % (total_disk_usage)), style)
    
    book.save(excel_file)
    return
    
if __name__ == "__main__" :

    setup_usages(input_file = "piadmin")
    print_usages()
    write_to_excel(excel_file = "admin-usage.xls", sheet = "admin usage")
    

    


#!/bin/env python

