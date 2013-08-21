#!/bin/env python

from sgestat import SGEStatistics
from diskusage import DiskUsage
from excel import *
from xlwt import Workbook
from chargerate import *
from utility import list_uniq
from invoice import create_invoice_for_pi_all
from invoice2 import create_invoice_for_pi_2

class HPCUsages :

    def __init__(self) :
        self.sge_statistics = None
        self.disk_usages = None
        return

    def create_disk_usages(self, home, cork, rio, oxford) :
        disk_usages = DiskUsage()
        disk_usages.create_usage_from_file(input_file = home, usage = disk_usages.home)
        disk_usages.create_usage_from_file(input_file = cork, usage = disk_usages.cork)
        disk_usages.create_usage_from_file(input_file = rio, usage = disk_usages.rio)
        disk_usages.create_usage_from_file(input_file = oxford, usage = disk_usages.oxford)
        disk_usages.setup_disk_users()
        disk_usages.assign_pi_to_disk_users()
        disk_usages.calculate_total_disk_usage_from_all_pis()
        disk_usages.calculate_total_disk_usage_from_all_users()
        self.disk_usages = disk_usages
        return

    def create_sge_statistics(self, sge_file) :
        self.sge_statistics = SGEStatistics(sge_file = sge_file)
        return

    def write_to_excel_file(self, excel_file = 'hpc-usage.xls') :

        sge_users = self.sge_statistics.sge_users
        disk_users = self.disk_usages.disk_users

        hpc_pis = self.sge_statistics.hpc_pis

        book = Workbook()
        sheet = book.add_sheet('HPC usage')
        sheet.portrait = False
        sheet.set_paper_size_code(1)
        #sheet.preview_magn = 150
        #sheet.page_preview = False

        # First line: header line
        
        i = 0
        style = myeasyxf(colour = (i+1)%2, borders='mdmn')
        sheet.write(i, 0, "PI", style)

        sheet.write(i, 1, "ID", style)
        sheet.write(i, 2, "Grant Number", style)

        style = myeasyxf(colour = (i+1)%2, borders='mdtn')
        sheet.write(i, 3, "CPU", style)
        sheet.write(i, 4, "CPU charge", style)

        style = myeasyxf(colour = (i+1)%2, borders='mddn')
        sheet.write(i, 5, "Disk", style)

        style = myeasyxf(colour = (i+1)%2, borders='mdtn')
        sheet.write(i, 6, "Disk charge", style)

        style = myeasyxf(colour = (i+1)%2, borders='mddn')
        sheet.write(i, 7, "Total charge", style)

        style = myeasyxf(colour = (i+1)%2, borders='mdtn')
        
        sheet.write(i, 8, "User", style)
        sheet.write(i, 9, "Name", style)
        
        sheet.write(i, 10, "CPU time", style)
        sheet.write(i, 11, "CPU Charge", style)
        sheet.write(i, 12, "Wall time", style)
        sheet.write(i, 13, "Memory", style)

        style = myeasyxf(colour = (i+1)%2, borders='mddn')
        sheet.write(i, 14, "home", style)

        style = myeasyxf(colour = (i+1)%2, borders='mdtn')
        sheet.write(i, 15, "cork", style)
        sheet.write(i, 16, "rio", style)
        sheet.write(i, 17, "oxford", style)
        sheet.write(i, 18, "Disk charge", style)
        
        style = myeasyxf(colour = (i+1)%2, borders='mddm')
        sheet.write(i, 19, "Total charge", style)

        i += 1
    
        i_pi = 0
        for pi in hpc_pis.keys() :
            
            if hpc_pis[pi].sge_members or hpc_pis[pi].disk_members :
                i_pi += 1
                hpc_members = list_uniq(hpc_pis[pi].sge_members + hpc_pis[pi].disk_members)
                n_members = len(hpc_members)
                
                style = myeasyxf(colour = 0, borders='ntmn')
                sheet.write_merge(r1=i, c1=0, r2=i+n_members-1, c2=0,
                              label=hpc_pis[pi].name, style=style)

                style = myeasyxf(colour = 0, borders='nttn')


                sheet.write_merge(r1=i, c1=1, r2=i+n_members-1, c2=1,
                                  label=pi,
                                  style=style)
                sheet.write_merge(r1=i, c1=2, r2=i+n_members-1, c2=2,
                                  label=None,
                                  style=style)
                
                sheet.write_merge(r1=i, c1=3, r2=i+n_members-1, c2=3,
                                  label=float("%.2f" % (hpc_pis[pi].cpu/3600)),
                                  style=style)
                sheet.write_merge(r1=i, c1=4, r2=i+n_members-1, c2=4,
                                  label=float("%.2f" % (hpc_pis[pi].cpu/3600*cpu_time_charge_per_hour)),
                                  style=style)

                style = myeasyxf(colour = 0, borders='ntdn')
                sheet.write_merge(r1=i, c1=5, r2=i+n_members-1, c2=5,
                                  label=float("%.2f" % (hpc_pis[pi].disk_space)),
                                  style=style)

                style = myeasyxf(colour = 0, borders='nttn')
                sheet.write_merge(r1=i, c1=6, r2=i+n_members-1, c2=6,
                                  label=float("%.2f" % (hpc_pis[pi].disk_charge)),
                                  style=style)
                
                style = myeasyxf(colour = 0, borders='ntdn')
                sheet.write_merge(r1=i, c1=7, r2=i+n_members-1, c2=7,
                                  label=float("%.2f" % (hpc_pis[pi].cpu/3600*cpu_time_charge_per_hour + hpc_pis[pi].disk_charge)),
                                  style=style)

                # For SGE and disk users with PI

                i_mem = 0
                for hpc_mem in hpc_members :
                    i_mem += 1
                    sge_user = None
                    disk_user = None
                    owner = None
                    name = None

                    if sge_users.has_key(hpc_mem) :
                        sge_user = sge_users[hpc_mem]
                        owner = sge_user.owner
                        name = sge_user.name
                        
                    if disk_users.has_key(hpc_mem) :
                        disk_user = disk_users[hpc_mem]
                        owner = disk_user.owner
                        name = disk_user.name

                    style = myeasyxf(colour = (i+1)%2, borders='nntn')
                    if i_mem == n_members :
                        style = myeasyxf(colour = (i+1)%2, borders='nttn')
                    sheet.write(i, 8, owner, style)
                    sheet.write(i, 9, name, style)
                    
                    if sge_user :
                        sheet.write(i, 10, float("%.2f" % (sge_user.cpu/3600)), style)
                        sheet.write(i, 11, float("%.2f" % (sge_user.cpu/3600*cpu_time_charge_per_hour)), style)
                        sheet.write(i, 12, float("%.2f" % (sge_user.wall_clock/3600)), style)
                        sheet.write(i, 13, float("%.2f" % (sge_user.memory/1.0e9)), style)
                    else :
                        sheet.write(i, 10, None, style)
                        sheet.write(i, 11, None, style)
                        sheet.write(i, 12, None, style)
                        sheet.write(i, 13, None, style)

                    if disk_user :
                        style = myeasyxf(colour = (i+1)%2, borders='nndn')
                        if i_mem == n_members :
                            style = myeasyxf(colour = (i+1)%2, borders='ntdn')

                        if disk_user.home :
                            sheet.write(i, 14, float("%.2f" % (disk_user.home)), style)
                        else :
                            sheet.write(i, 14, None, style)

                        style = myeasyxf(colour = (i+1)%2, borders='nntn')
                        if i_mem == n_members :
                            style = myeasyxf(colour = (i+1)%2, borders='nttn')
                
                        if disk_user.cork :
                            sheet.write(i, 15, float("%.2f" % (disk_user.cork)), style)
                        else :
                            sheet.write(i, 15, None, style)

                        if disk_user.rio :
                            sheet.write(i, 16, float("%.2f" % (disk_user.rio)), style)
                        else :
                            sheet.write(i, 16, None, style)

                        if disk_user.oxford :
                            sheet.write(i, 17, float("%.2f" % (disk_user.oxford)), style)
                        else :
                            sheet.write(i, 17, None, style)
                
                        if disk_user.charge :
                            sheet.write(i, 18, float("%.2f" % (disk_user.charge)), style)
                        else :
                            sheet.write(i, 18, None, style)
                    else :
                        style = myeasyxf(colour = (i+1)%2, borders='nndn')
                        if i_mem == n_members :
                            style = myeasyxf(colour = (i+1)%2, borders='ntdn')
                        sheet.write(i, 14, None, style)
                        style = myeasyxf(colour = (i+1)%2, borders='nntn')
                        if i_mem == n_members :
                            style = myeasyxf(colour = (i+1)%2, borders='nttn')
                        sheet.write(i, 15, None, style)
                        sheet.write(i, 16, None, style)
                        sheet.write(i, 17, None, style)
                        sheet.write(i, 18, None, style)

                    total_charge = 0
                    if sge_user :
                        total_charge += sge_user.cpu/3600*cpu_time_charge_per_hour
                    if disk_user :
                        total_charge += disk_user.charge
                        
                    style = myeasyxf(colour = (i+1)%2, borders='nndm')
                    if i_mem == n_members :
                        style = myeasyxf(colour = (i+1)%2, borders='ntdm')
                    sheet.write(i, 19, float("%.2f" % (total_charge)), style)

                    i += 1

        # For SGE + disk users without PI

        hpc_members = list_uniq(sge_users.keys() + disk_users.keys())
        for hpc_mem in hpc_members :
            sge_user = None
            disk_user = None
            owner = None
            name = None

            if sge_users.has_key(hpc_mem) :
                sge_user = sge_users[hpc_mem]
                owner = sge_user.owner
                name = sge_user.name
                if sge_user.pi : continue
                
            if disk_users.has_key(hpc_mem) :
                disk_user = disk_users[hpc_mem]
                owner = disk_user.owner
                name = disk_user.name
                if disk_user.pi : continue

            if owner == "root" or owner == "pinetest" or \
                   owner == "apache" or owner == "nfsnobody" :
                continue

            style = myeasyxf(colour = (i+1)%2, borders='ntmn')
            sheet.write(i, 0, None, style)

            style = myeasyxf(colour = (i+1)%2, borders='nttn')
            sheet.write(i, 1, None, style)
            sheet.write(i, 2, None, style)
            sheet.write(i, 3, None, style)
            sheet.write(i, 4, None, style)
            sheet.write(i, 5, None, style)
            sheet.write(i, 6, None, style)
            sheet.write(i, 7, None, style)

            #style = myeasyxf(colour = (i+1)%2, borders='nttn')
            sheet.write(i, 8, owner, style)
            sheet.write(i, 9, name, style)

            if sge_user :
                sheet.write(i, 10, float("%.2f" % (sge_user.cpu/3600)), style)
                sheet.write(i, 11, float("%.2f" % (sge_user.cpu/3600*cpu_time_charge_per_hour)), style)
                sheet.write(i, 12, float("%.2f" % (sge_user.wall_clock/3600)), style)
                sheet.write(i, 13, float("%.2f" % (sge_user.memory/1.0e9)), style)
            else :
                sheet.write(i, 10, None, style)
                sheet.write(i, 11, None, style)
                sheet.write(i, 12, None, style)
                sheet.write(i, 13, None, style)

            if disk_user :
                style = myeasyxf(colour = (i+1)%2, borders='ntdn')
                if disk_user.home :
                    sheet.write(i, 14, float("%.2f" % (disk_user.home)), style)
                else :
                    sheet.write(i, 14, None, style)
                    
                style = myeasyxf(colour = (i+1)%2, borders='nttn')
                if disk_user.cork :
                    sheet.write(i, 15, float("%.2f" % (disk_user.cork)), style)
                else :
                    sheet.write(i, 15, None, style)

                if disk_user.rio :
                    sheet.write(i, 16, float("%.2f" % (disk_user.rio)), style)
                else :
                    sheet.write(i, 16, None, style)

                if disk_user.oxford :
                    sheet.write(i, 17, float("%.2f" % (disk_user.oxford)), style)
                else :
                    sheet.write(i, 17, None, style)
                
                if disk_user.charge :
                    sheet.write(i, 18, float("%.2f" % (disk_user.charge)), style)
                else :
                    sheet.write(i, 18, None, style)
            else :
                style = myeasyxf(colour = (i+1)%2, borders='ntdn')
                sheet.write(i, 14, None, style)
                style = myeasyxf(colour = (i+1)%2, borders='nttn')
                sheet.write(i, 15, None, style)
                sheet.write(i, 16, None, style)
                sheet.write(i, 17, None, style)
                sheet.write(i, 18, None, style)
                
            total_charge = 0
            if sge_user :
                total_charge += sge_user.cpu/3600*cpu_time_charge_per_hour
            if disk_user :
                total_charge += disk_user.charge
                        
            style = myeasyxf(colour = (i+1)%2, borders='ntdm')
            sheet.write(i, 19, float("%.2f" % (total_charge)), style)

            i += 1

        # last line

        style = myeasyxf(colour = (i+1)%2, borders='dmmn')
        sheet.write(i, 0, "Total", style)

        style = myeasyxf(colour = (i+1)%2, borders='dmtn')
        sheet.write(i, 1, None, style)
        sheet.write(i, 2, None, style)
        sheet.write(i, 3, None, style)
        sheet.write(i, 4, None, style)
        sheet.write(i, 5, None, style)
        sheet.write(i, 6, None, style)
        sheet.write(i, 7, None, style)
        sheet.write(i, 8, None, style)
        sheet.write(i, 9, None, style)
        sheet.write(i, 10, None, style)
        sheet.write(i, 11, None, style)
        sheet.write(i, 12, None, style)
        sheet.write(i, 13, None, style)

        style = myeasyxf(colour = (i+1)%2, borders='dmdn')
        sheet.write(i, 14, None, style)

        style = myeasyxf(colour = (i+1)%2, borders='dmtn')
        sheet.write(i, 15, None, style)
        sheet.write(i, 16, None, style)
        sheet.write(i, 17, None, style)
        sheet.write(i, 18, None, style)

        style = myeasyxf(colour = (i+1)%2, borders='dmdm')
        sheet.write(i, 19, None, style)

        book.save(excel_file)
        return

    def write_to_excel_file_2(self, excel_file = 'PI-usage.xls') :

        sge_users = self.sge_statistics.sge_users
        disk_users = self.disk_usages.disk_users

        hpc_pis =self.sge_statistics.hpc_pis

        book = Workbook()
        sheet = book.add_sheet('HPC PI usage')
        sheet.portrait = False
        sheet.set_paper_size_code(1)
        #sheet.preview_magn = 150
        #sheet.page_preview = True

        # First line: header line
        
        i = 0
        style = myeasyxf(colour = (i+1)%2, borders='mdmn')
        sheet.write(i, 0, "PI", style)

        style = myeasyxf(colour = (i+1)%2, borders='mdtn')
        sheet.write(i, 1, "UserID", style)
        sheet.write(i, 2, "Name", style)
        sheet.write(i, 3, "CPU (hour)", style)
        sheet.write(i, 4, "Wall time (hour)", style)
        sheet.write(i, 5, "Memory (10e9 GB)", style)
        sheet.write(i, 6, "home (GB)", style)
        sheet.write(i, 7, "cork (GB)", style)
        sheet.write(i, 8, "rio (GB)", style)

        style = myeasyxf(colour = (i+1)%2, borders='mdtm')
        sheet.write(i, 9, "oxford (GB)", style)

        i += 1

        i_pi = 0
        for pi in hpc_pis.keys() :
            if hpc_pis[pi].sge_members or hpc_pis[pi].disk_members :
                i_pi += 1
                hpc_members = list_uniq(hpc_pis[pi].sge_members + hpc_pis[pi].disk_members)
                n_members = len(hpc_members)

                # whilte row
                style = myeasyxf(colour = 0, borders='nmnn')
                for j in xrange(0, 10) :
                    sheet.write(i, j, None, style)
                i += 1
                
                style = myeasyxf(colour = 0, borders='ntmn')
                sheet.write_merge(r1=i, c1=0, r2=i+n_members-1, c2=0,
                                  label=hpc_pis[pi].name, style=style)

                _total_cpu = 0
                _total_wall_time = 0
                _total_memory = 0
                _total_home = 0
                _total_cork = 0
                _total_rio = 0
                _total_oxford = 0
                                
                # For SGE and disk users with PI
                
                i_mem = 0
                for hpc_mem in hpc_members :
                    i_mem += 1
                    sge_user = None
                    disk_user = None
                    owner = None
                    name = None

                    if sge_users.has_key(hpc_mem) :
                        sge_user = sge_users[hpc_mem]
                        owner = sge_user.owner
                        name = sge_user.name
                        
                    if disk_users.has_key(hpc_mem) :
                        disk_user = disk_users[hpc_mem]
                        owner = disk_user.owner
                        name = disk_user.name

                    style = myeasyxf(colour = (i+1)%2, borders='nntn')
                    sheet.write(i, 1, owner, style)
                    sheet.write(i, 2, name, style)
                    
                    if sge_user :
                        sheet.write(i, 3, float("%.2f" % (sge_user.cpu/3600)), style)
                        sheet.write(i, 4, float("%.2f" % (sge_user.wall_clock/3600)), style)
                        sheet.write(i, 5, float("%.2f" % (sge_user.memory/1.0e9)), style)
                        _total_cpu += sge_user.cpu/3600
                        _total_wall_time += sge_user.wall_clock/3600
                        _total_memory += sge_user.memory/1.0e9
                    else :
                        sheet.write(i, 3, None, style)
                        sheet.write(i, 4, None, style)
                        sheet.write(i, 5, None, style)

                    if disk_user :
                        style = myeasyxf(colour = (i+1)%2, borders='nndn')

                        if disk_user.home :
                            sheet.write(i, 6, float("%.2f" % (disk_user.home)), style)
                            _total_home += disk_user.home
                        else :
                            sheet.write(i, 6, None, style)

                        style = myeasyxf(colour = (i+1)%2, borders='nntn')
                
                        if disk_user.cork :
                            sheet.write(i, 7, float("%.2f" % (disk_user.cork)), style)
                            _total_cork += disk_user.cork
                        else :
                            sheet.write(i, 7, None, style)

                        style = myeasyxf(colour = (i+1)%2, borders='nntn')
                        if disk_user.rio :
                            sheet.write(i, 8, float("%.2f" % (disk_user.rio)), style)
                            _total_rio += disk_user.rio
                        else :
                            sheet.write(i, 8, None, style)

                        style = myeasyxf(colour = (i+1)%2, borders='nntm')
                        if disk_user.oxford :
                            sheet.write(i, 9, float("%.2f" % (disk_user.oxford)), style)
                            _total_oxford += disk_user.oxford
                        else :
                            sheet.write(i, 9, None, style)
                
                    else :
                        style = myeasyxf(colour = (i+1)%2, borders='nndn')
                        sheet.write(i, 6, None, style)
                        style = myeasyxf(colour = (i+1)%2, borders='nntn')
                        sheet.write(i, 7, None, style)
                        style = myeasyxf(colour = (i+1)%2, borders='nntn')
                        sheet.write(i, 8, None, style)
                        style = myeasyxf(colour = (i+1)%2, borders='nntm')
                        sheet.write(i, 9, None, style)

                    i += 1
                        
                # total line

                style = myeasyxf(colour = 1, borders='dmmn')
                sheet.write(i, 0, "Total", style)

                style = myeasyxf(colour = 1, borders='dmtn')
                sheet.write(i, 1, None, style)
                sheet.write(i, 2, None, style)

                if _total_cpu :
                    sheet.write(i, 3, float("%.2f" % (_total_cpu)), style)
                else :
                     sheet.write(i, 3, None, style)

                if _total_wall_time :
                    sheet.write(i, 4, float("%.2f" % (_total_wall_time)), style)
                else :
                    sheet.write(i, 4, None, style)

                if _total_memory :
                    sheet.write(i, 5, float("%.2f" % (_total_memory)), style)
                else :
                    sheet.write(i, 5, None, style)

                style = myeasyxf(colour = 1, borders='dmdn')
                if _total_home :
                    sheet.write(i, 6, float("%.2f" % (_total_home)), style)
                else :
                    sheet.write(i, 6, None, style)

                style = myeasyxf(colour = 1, borders='dmtn')
                if _total_cork :
                    sheet.write(i, 7, float("%.2f" % (_total_cork)), style)
                else :
                    sheet.write(i, 7, None, style)

                style = myeasyxf(colour = 1, borders='dmtn')
                if _total_rio :
                    sheet.write(i, 8, float("%.2f" % (_total_rio)), style)
                else :
                    sheet.write(i, 8, None, style)
                
                style = myeasyxf(colour = 1, borders='dmtm')
                if _total_oxford :
                    sheet.write(i, 9, float("%.2f" % (_total_oxford)), style)
                else :
                    sheet.write(i, 9, None, style)
                
                i += 1
                
        book.save(excel_file)
        return

    def create_invoices(self) :
        print " Create invoice"
        hpc_pis =self.sge_statistics.hpc_pis
        """
        i_pi = 16
        pi = 'cbranch'
        create_invoice_for_pi(hpc_pis[pi], pi_index= i_pi,
                              sge_users = self.sge_statistics.sge_users,
                              disk_users = self.disk_usages.disk_users)

        return
        """
        total_charge = 0.0
        i_pi = 0
        for pi in hpc_pis.keys() :
            i_pi += 1
            total_charge += create_invoice_for_pi_all(hpc_pis[pi], pi_index= i_pi,
                                                      sge_users = self.sge_statistics.sge_users,
                                                      disk_users = self.disk_usages.disk_users)
        print 'Total charge for all $%.2f' % total_charge
        return

    def create_invoices_2(self) :
        print " Create invoice"
        hpc_pis =self.sge_statistics.hpc_pis

        #i_pi = 16
        #pi = 'bergman'
        #create_invoice_for_pi_2(hpc_pis[pi], pi_index= i_pi,
        #                        sge_users = self.sge_statistics.sge_users,
        #                        disk_users = self.disk_usages.disk_users)
        
        #return

        total_charge = 0.0
        i_pi = 0
        for pi in hpc_pis.keys() :
            i_pi += 1
            charge = create_invoice_for_pi_2(hpc_pis[pi], pi_index= i_pi,
                                             sge_users = self.sge_statistics.sge_users,
                                             disk_users = self.disk_usages.disk_users)
            total_charge += charge
        print 'Total charge for CPU + scratch: $%.2f' % total_charge
        return
        
if __name__ == "__main__" :
    print " This is my HPC usage test"

    hpc_usages = HPCUsages()
    hpc_usages.create_sge_statistics(sge_file = ["albert.usage", "chaim.usage"])
    hpc_usages.create_disk_usages(home="home", cork="cork", rio="rio", oxford="oxford")

    hpc_usages.write_to_excel_file()
    hpc_usages.write_to_excel_file_2()

    hpc_usages.create_invoices()
    hpc_usages.create_invoices_2()
