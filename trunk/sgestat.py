#!/bin/env python

from sgeuser import sge_users
from hpcpi import hpc_pis
from excel import *
from xlwt import Workbook

from chargerate import cpu_time_charge_per_hour 

class SGEStatistics :

    def __init__(self, begin = None, end = None, sge_file = None) :
        self.total_cpu_from_all_users = 0
        self.total_cpu_from_all_pis = 0

        self.sge_users = sge_users(begin=begin, end=end, sge_qacct_output_file=sge_file)
        self.hpc_pis = hpc_pis()

        self.assgin_pi_to_sge_users()
        self.calculate_total_cpu_from_all_users()
        self.calculate_total_cpu_from_all_pis()

        return

    def assgin_pi_to_sge_users(self) :
        for user in self.sge_users.keys() :
            found_pi = 0
            for pi in self.hpc_pis.keys() :
                if found_pi : break
                for member in self.hpc_pis[pi].members :
                    if member == self.sge_users[user].owner :
                        self.sge_users[user].pi = pi
                        self.hpc_pis[pi].sge_members.append(member)
                        found_pi = 1
                        break
        return

    def calculate_total_cpu_from_all_users(self) :
        self.total_cpu_from_all_users = 0
        for user in self.sge_users.keys() :
            self.total_cpu_from_all_users += self.sge_users[user].cpu
        return

    def calculate_total_cpu_from_all_pis(self) :
        self.total_cpu_from_all_pis = 0
        for pi in self.hpc_pis.keys() :
            self.hpc_pis[pi].cpu = 0
            for member in self.hpc_pis[pi].sge_members :
                self.hpc_pis[pi].cpu += self.sge_users[member].cpu
            self.total_cpu_from_all_pis += self.hpc_pis[pi].cpu
        return

    def write_to_excel_file(self, excel_file = 'sge-usage.xls') :

        sge_users = self.sge_users
        hpc_pis = self.hpc_pis
        total_cpu_from_all_users = self.total_cpu_from_all_users
        total_cpu_from_all_pis = self.total_cpu_from_all_pis

        book = Workbook()
        sheet = book.add_sheet('SGE usage')
        sheet.portrait = False
        sheet.set_paper_size_code(1)

        i = 0
        style = myeasyxf(colour = (i+1)%2, borders='mdmn')
        sheet.write(i, 0, "PI", style)

        style = myeasyxf(colour = (i+1)%2, borders='mdtn')
        sheet.write(i, 1, "CPU time", style)
        sheet.write(i, 2, "Charge", style)
        sheet.write(i, 3, "User", style)
        sheet.write(i, 4, "Name", style)
        sheet.write(i, 5, "CPU time", style)
        sheet.write(i, 6, "Charge", style)
        sheet.write(i, 7, "Wall time", style)

        style = myeasyxf(colour = (i+1)%2, borders='mdtm')
        sheet.write(i, 8, "Memory", style)
        i += 1

        i_pi = 0
        for pi in hpc_pis.keys() :
            if hpc_pis[pi].sge_members :
                i_pi += 1
                n_members = len(hpc_pis[pi].sge_members)

                style = myeasyxf(colour = 0, borders='ntmn')
                sheet.write_merge(r1=i, c1=0, r2=i+n_members-1, c2=0,
                                  label=hpc_pis[pi].name, style=style)

                style = myeasyxf(colour = 0, borders='nttn')
                sheet.write_merge(r1=i, c1=1, r2=i+n_members-1, c2=1,
                                  label=float("%.2f" % (hpc_pis[pi].cpu/3600)),
                                  style=style)
                sheet.write_merge(r1=i, c1=2, r2=i+n_members-1, c2=2,
                                  label=float("%.2f" % (hpc_pis[pi].cpu/3600*cpu_time_charge_per_hour)),
                                  style=style)

                i_mem = 0
                for sge_mem in hpc_pis[pi].sge_members :
                    i_mem += 1
                    sge_user = sge_users[sge_mem]
                    style = myeasyxf(colour = (i+1)%2, borders='nntn')
                    if i_mem == n_members :
                        style = myeasyxf(colour = (i+1)%2, borders='nttn')
                    sheet.write(i, 3, sge_user.owner, style)
                    sheet.write(i, 4, sge_user.name, style)
                    sheet.write(i, 5, float("%.2f" % (sge_user.cpu/3600)), style)
                    sheet.write(i, 6, float("%.2f" % (sge_user.cpu/3600*cpu_time_charge_per_hour)), style)
                    sheet.write(i, 7, float("%.2f" % (sge_user.wall_clock/3600)), style)

                    style = myeasyxf(colour = (i+1)%2, borders='nntm')
                    if i_mem == n_members :
                        style = myeasyxf(colour = (i+1)%2, borders='nttm')
                    sheet.write(i, 8, float("%.2f" % (sge_user.memory/1.0e9)), style)

                    i += 1

        for user in sge_users.keys() :
            sge_user = sge_users[user]
            if sge_user.pi :
                continue

            style = myeasyxf(colour = (i+1)%2, borders='ntmn')
            sheet.write(i, 0, None, style)

            style = myeasyxf(colour = (i+1)%2, borders='nttn')
            sheet.write(i, 1, None, style)
            sheet.write(i, 2, None, style)
            sheet.write(i, 3, sge_user.owner, style)
            sheet.write(i, 4, sge_user.name, style)
            sheet.write(i, 5, float("%.2f" % (sge_user.cpu/3600)), style)
            sheet.write(i, 6, float("%.2f" % (sge_user.cpu/3600*cpu_time_charge_per_hour)), style)
            sheet.write(i, 7, float("%.2f" % (sge_user.wall_clock/3600)), style)

            style = myeasyxf(colour = (i+1)%2, borders='nttm')
            sheet.write(i, 8, float("%.2f" % (sge_user.memory/1.0e9)), style)

            i += 1

        style = myeasyxf(colour = (i+1)%2, borders='dmmn')
        sheet.write(i, 0, "Total", style)

        style = myeasyxf(colour = (i+1)%2, borders='dmtn')
        sheet.write(i, 1, float("%.2f" % (self.total_cpu_from_all_pis/3600)), style)
        sheet.write(i, 2, float("%.2f" % (self.total_cpu_from_all_pis/3600*cpu_time_charge_per_hour)), style)
        sheet.write(i, 3, None, style)
        sheet.write(i, 4, None, style)
        sheet.write(i, 5, float("%.2f" % (self.total_cpu_from_all_users/3600)), style)
        sheet.write(i, 6, float("%.2f" % (self.total_cpu_from_all_users/3600*cpu_time_charge_per_hour)), style)
        sheet.write(i, 7, None, style)

        style = myeasyxf(colour = (i+1)%2, borders='dmtm')
        sheet.write(i, 8, None, style)

        book.save(excel_file)
        return

if __name__ == "__main__" :

    sge_stats = SGEStatistics(sge_file = ["albert.usage", "chaim.usage"])
    sge_stats.write_to_excel_file()

    
