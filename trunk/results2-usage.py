#!/bin/env python

from utility import check_file_exists, is_blank_line
from excel import *
from xlwt import Workbook
from chargerate import charge_rate

class Results2PI :
    
    def __init__(self, line = None) :
        self.name = None
        self.credential = None
        self.grant = None
        self.results2_id = None
        if line :
            tmp = line.split(":")
            assert len(tmp) == 3
            self.name = tmp[0]
            self.credential = tmp[1]
            self.results2_id = tmp[2]
        return

    def __repr__(self) :
        s = ""
        if self.name : s += " Name: " + self.name
        if self.credential : s += " Credential: " + self.credential
        if self.grant : s += " Grant: " + self.grant
        if self.results2_id : s += " Results2: " + self.results2_id
        return s

_results2_pis = None

def results2_pis() :
    global _results2_pis
    if not _results2_pis :
        _results2_pis = {}
        pi_hash_table_file = "/cork/dicom/ad-lin-results2"
        check_file_exists(pi_hash_table_file)

        print " Reading from file: " + pi_hash_table_file

        fin = open(pi_hash_table_file, "r")
        assert fin
        while 1 :
            line = fin.readline()
            if not line : break
            line = line.strip()
            if is_blank_line(line) : continue
            results2_pi = Results2PI(line)
            _results2_pis[results2_pi.results2_id] = results2_pi 

        fin.close()

    return _results2_pis


class Results2Usages :

    def __init__(self) :
        self.ids = {}
        return

    def add_pi(self, results2_id, size) :
        self.ids[results2_id] = size
        return

    def write_to_excel(self, excel_file = 'results2-usage.xls') :

        book = Workbook()
        sheet = book.add_sheet('results2 usage')
        sheet.portrait = False
        sheet.set_paper_size_code(1)
        
        i = 0
        style = myeasyxf(colour = (i+1)%2, borders='mdmn')
        sheet.write(i, 0, "PI (name)", style)

        style = myeasyxf(colour = (i+1)%2, borders='mdtn')
        sheet.write(i, 1, "AD Credential", style)
        sheet.write(i, 2, "Grant Number", style)
        sheet.write(i, 3, "Results2 ID", style)
        sheet.write(i, 4, "Results2 (GB)", style)

        style = myeasyxf(colour = (i+1)%2, borders='mdtm')
        sheet.write(i, 5, "Charge", style)
        i += 1

        total_size = 0
        
        for results2_id in sorted(self.ids.keys()) :
            if results2_pis().has_key(results2_id) :
                disk_size = self.ids[results2_id]
                pi =  results2_pis()[results2_id]
                style = myeasyxf(colour = (i+1)%2, borders='nnmn')
                sheet.write(i, 0, pi.name, style)

                style = myeasyxf(colour = (i+1)%2, borders='nntn')
                sheet.write(i, 1, pi.credential, style)
                sheet.write(i, 2, pi.grant, style)
                sheet.write(i, 3, pi.results2_id, style)
                sheet.write(i, 4, float("%.2f" % (disk_size)), style)

                style = myeasyxf(colour = (i+1)%2, borders='nntm')
                sheet.write(i, 5, float("%.2f" % (disk_size*charge_rate)), style)

                total_size += disk_size

                i += 1
            else :
                print " No PI for " + results2_id

        style = myeasyxf(colour = (i+1)%2, borders='dmmn')
        sheet.write(i, 0, "Total", style)

        style = myeasyxf(colour = (i+1)%2, borders='dmtn')
        sheet.write(i, 1, None, style)
        sheet.write(i, 2, None, style)
        sheet.write(i, 3, None, style)
        sheet.write(i, 4, float("%.2f" % (total_size)), style)

        style = myeasyxf(colour = (i+1)%2, borders='dmtm')
        sheet.write(i, 5, float("%.2f" % (total_size*charge_rate)), style)
        
        book.save(excel_file)
        return
        
if __name__ == "__main__" :

    results2_usage = Results2Usages()
    
    usage_file = 'results2pi'
    check_file_exists(usage_file)

    fin = open(usage_file, "r")
    assert fin
    while 1 :
        line = fin.readline()
        if not line : break
        if is_blank_line(line) : continue
        line = line.strip()
        tmp = line.split()
        assert len(tmp) == 2
        size = float(tmp[0])
        tmp = tmp[1].split('/')
        results2_id = tmp[-1]
        results2_usage.add_pi(results2_id = results2_id, size = size)

    fin.close()

    results2_usage.write_to_excel()
