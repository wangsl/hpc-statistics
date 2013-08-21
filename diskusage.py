#!/bin/env python

import os, pwd
from os import path
from utility import check_file_exists, list_uniq
from fullname import hpc_users_with_full_name
from hpcpi import hpc_pis
from excel import *
from xlwt import Workbook
from unknownfiles import unknown_files

from chargerate import home_charge_rate, replication_charge_rate, free_home_space, scratch_charge_rate

class DiskUser :
    def __init__(self) :
        self.owner = None
        self.name = None
        self.pi = None
        self.home = None
        self.cork = None
        self.rio = None
        self.oxford=None
        self.charge = None
        self.space = None
        return

    def calculate_charge(self) :
        self.charge = 0
        self.space = 0
        if self.home :
            self.space += self.home
            if self.home > free_home_space :
                self.charge += (self.home - free_home_space)*home_charge_rate
                self.charge += (self.home - free_home_space)*replication_charge_rate

        if self.cork :
            self.space += self.cork
            self.charge += self.cork*scratch_charge_rate

        if self.rio :
            self.space += self.rio
            self.charge += self.rio*scratch_charge_rate

        if self.oxford :
            self.space += self.oxford
            self.charge += self.oxford*scratch_charge_rate

        return

    def __repr__(self) :
        s = ""
        if self.owner : s += " Owner: " + self.owner
        if self.name : s += " Name: " + self.name
        if self.pi : s += " PI: " + self.pi
        if self.home : s += " Home: " + ("%.2f" % (self.home))
        if self.cork : s += " Cork: " + ("%.2f" % (self.cork))
        if self.rio : s += " Rio: " + ("%.2f" % (self.rio))
        if self.oxford : s+= "Oxford: " + ("%.2f" % (self.oxford))
        if self.space : s += " Space: " + ("%.2f" % (self.space))
        if self.charge : s += " Charge: " + ("%.2f" % (self.charge))
        return s

class DiskUsage :
    def __init__(self) :
        self.disk_users = {}
        self.hpc_pis = hpc_pis()

        self.total_disk_space_from_all_pis = 0
        self.total_disk_charge_from_all_pis = 0

        self.home = {}
        self.cork = {}
        self.rio = {}
        self.oxford = {}
        return

    def create_usage_from_file(self, input_file, usage) :
        check_file_exists(input_file)

        fin = open(input_file, "r")
        assert fin
        while 1 :
            line = fin.readline()
            if not line : break
            line = line.strip()
            tmp = line.split()
            assert len(tmp) >= 2
            size = float(tmp[0])
            folder = tmp[1]
            if path.exists(folder) :
                stat_info = os.stat(folder)
                uid = stat_info.st_uid
                try :
                    owner = pwd.getpwuid(uid)[0]
                except :
                    if unknown_files().has_key(tmp[1]) :
                        owner = unknown_files()[tmp[1]]
                    else :
                        owner = tmp[1]
                    
                if usage.has_key(owner) :
                    usage[owner] += size
                else :
                    usage[owner] = size
        fin.close()
        return

    def setup_disk_users(self) :
        self.disk_users = {}
        users = []
        if self.home : users += self.home.keys()
        if self.cork : users += self.cork.keys()
        if self.rio : users += self.rio.keys()
        if self.oxford: users += self.oxford.keys()

        users = list_uniq(users)

        hpc_users = hpc_users_with_full_name()

        for user in users :
            disk_user = DiskUser()

            disk_user.owner = user

            if hpc_users.has_key(user) :
                disk_user.name = hpc_users[user]
            
            if self.home.has_key(user) :
                disk_user.home = self.home[user]
            if self.cork.has_key(user) :
                disk_user.cork = self.cork[user]
            if self.rio.has_key(user) :
                disk_user.rio = self.rio[user]
            if self.oxford.has_key(user) :
                disk_user.oxford = self.oxford[user]

            disk_user.calculate_charge()

            self.disk_users[user] = disk_user
        return

    def assign_pi_to_disk_users(self) :
        for user in self.disk_users.keys() :
            found_pi = 0
            for pi in self.hpc_pis.keys() :
                if found_pi : break
                for member in self.hpc_pis[pi].members :
                    if member == self.disk_users[user].owner :
                        self.disk_users[user].pi = pi
                        self.hpc_pis[pi].disk_members.append(member)
                        found_pi = 1
                        break
        return

    
    def calculate_total_disk_usage_from_all_pis(self) :
        self.total_disk_space_from_all_pis = 0
        self.total_disk_charge_from_all_pis = 0
        for pi in self.hpc_pis.keys() :
            self.hpc_pis[pi].disk_space = 0
            self.hpc_pis[pi].disk_charge = 0
            for member in self.hpc_pis[pi].disk_members :
                self.hpc_pis[pi].disk_space += self.disk_users[member].space
                self.hpc_pis[pi].disk_charge += self.disk_users[member].charge
            self.total_disk_space_from_all_pis += self.hpc_pis[pi].disk_space
            self.total_disk_charge_from_all_pis += self.hpc_pis[pi].disk_charge
        return

    def calculate_total_disk_usage_from_all_users(self) :
        self.total_home_usage = 0
        self.total_cork_usage = 0
        self.total_rio_usage = 0
        self.total_oxford_usage = 0
        self.total_charge = 0
        for user in self.disk_users.keys() :
            disk_user = self.disk_users[user]
            if disk_user.home : self.total_home_usage += disk_user.home
            if disk_user.cork : self.total_cork_usage += disk_user.cork
            if disk_user.rio : self.total_rio_usage += disk_user.rio
            if disk_user.oxford : self.total_oxford_usage += disk_user.oxford
            if disk_user.charge : self.total_charge += disk_user.charge
        return

    def write_to_excel(self, excel_file = 'disk-usage.xls') :

        disk_users = self.disk_users
        hpc_pis = self.hpc_pis

        book = Workbook()
        sheet = book.add_sheet('disk usage')
        sheet.portrait = False
        sheet.set_paper_size_code(1)

        i = 0
        style = myeasyxf(colour = (i+1)%2, borders='mdmn')
        sheet.write(i, 0, "PI", style)

        style = myeasyxf(colour = (i+1)%2, borders='mdtn')
        sheet.write(i, 1, "Total Disk", style)
        sheet.write(i, 2, "Charge", style)
        sheet.write(i, 3, "User", style)
        sheet.write(i, 4, "Name", style)
        sheet.write(i, 5, "home", style)
        sheet.write(i, 6, "cork", style)
        sheet.write(i, 7, "rio", style)
        sheet.write(i, 8, "oxford", style)

        style = myeasyxf(colour = (i+1)%2, borders='mdtm')
        sheet.write(i, 9, "charge", style)
        i += 1

        i_pi = 0
        for pi in sorted(hpc_pis.keys()) :
            if hpc_pis[pi].disk_members :
                i_pi += 1
                n_members = len(hpc_pis[pi].disk_members)

                style = myeasyxf(colour = 0, borders='ntmn')
                sheet.write_merge(r1=i, c1=0, r2=i+n_members-1, c2=0,
                                  label=hpc_pis[pi].name, style=style)

                style = myeasyxf(colour = 0, borders='nttn')
                sheet.write_merge(r1=i, c1=1, r2=i+n_members-1, c2=1,
                                  label=float("%.2f" % (hpc_pis[pi].disk_space)),
                                  style=style)
                sheet.write_merge(r1=i, c1=2, r2=i+n_members-1, c2=2,
                                  label=float("%.2f" % (hpc_pis[pi].disk_charge)),
                                  style=style)

                i_mem = 0
                for disk_mem in sorted(hpc_pis[pi].disk_members) :
                    i_mem += 1
                    disk_user = disk_users[disk_mem]
                    style = myeasyxf(colour = (i+1)%2, borders='nntn')
                    if i_mem == n_members :
                        style = myeasyxf(colour = (i+1)%2, borders='nttn')
                    sheet.write(i, 3, disk_user.owner, style)
                    sheet.write(i, 4, disk_user.name, style)
                    
                    if disk_user.home :
                        sheet.write(i, 5, float("%.2f" % (disk_user.home)), style)
                    else :
                        sheet.write(i, 5, None, style)

                    if disk_user.cork :
                        sheet.write(i, 6, float("%.2f" % (disk_user.cork)), style)
                    else :
                        sheet.write(i, 6, None, style)

                    if disk_user.rio :
                        sheet.write(i, 7, float("%.2f" % (disk_user.rio)), style)
                    else :
                        sheet.write(i, 7, None, style)
                        
                    if disk_user.oxford :
                        sheet.write(i, 8, float("%.2f" % (disk_user.oxford)), style)
                    else :
                        sheet.write(i, 8, None, style)

                    style = myeasyxf(colour = (i+1)%2, borders='nntm')
                    if i_mem == n_members :
                        style = myeasyxf(colour = (i+1)%2, borders='nttm')
                    if disk_user.charge :
                        sheet.write(i, 9, float("%.2f" % (disk_user.charge)), style)
                    else :
                        sheet.write(i, 9, None, style)

                    i += 1
                    
        for user in sorted(disk_users.keys()) :
            disk_user = disk_users[user]

            if disk_user.pi : continue
            if not disk_user.name : continue

            style = myeasyxf(colour = (i+1)%2, borders='ntmn')
            sheet.write(i, 0, None, style)

            style = myeasyxf(colour = (i+1)%2, borders='nttn')
            sheet.write(i, 1, None, style)
            sheet.write(i, 2, None, style)
            sheet.write(i, 3, disk_user.owner, style)
            sheet.write(i, 4, disk_user.name, style)

            if disk_user.home :
                sheet.write(i, 5, float("%.2f" % (disk_user.home)), style)
            else :
                sheet.write(i, 5, None, style)
                
            if disk_user.cork :
                sheet.write(i, 6, float("%.2f" % (disk_user.cork)), style)
            else :
                sheet.write(i, 6, None, style)

            if disk_user.rio :
                sheet.write(i, 7, float("%.2f" % (disk_user.rio)), style)
            else :
                sheet.write(i, 7, None, style)

            if disk_user.oxford :
                sheet.write(i, 8, float("%.2f" % (disk_user.oxford)), style)
            else :
                sheet.write(i, 8, None, style)

            style = myeasyxf(colour = (i+1)%2, borders='nttm')
            if disk_user.charge :
                sheet.write(i, 9, float("%.2f" % (disk_user.charge)), style)
            else :
                sheet.write(i, 9, None, style)

            i += 1

        for user in sorted(disk_users.keys()) :
            disk_user = disk_users[user]

            if disk_user.pi : continue
            if disk_user.name : continue

            style = myeasyxf(colour = (i+1)%2, borders='ntmn')
            sheet.write(i, 0, None, style)

            style = myeasyxf(colour = (i+1)%2, borders='nttn')
            sheet.write(i, 1, None, style)
            sheet.write(i, 2, None, style)
            sheet.write(i, 3, disk_user.owner, style)
            sheet.write(i, 4, disk_user.name, style)

            if disk_user.home :
                sheet.write(i, 5, float("%.2f" % (disk_user.home)), style)
            else :
                sheet.write(i, 5, None, style)
                
            if disk_user.cork :
                sheet.write(i, 6, float("%.2f" % (disk_user.cork)), style)
            else :
                sheet.write(i, 6, None, style)

            if disk_user.rio :
                sheet.write(i, 7, float("%.2f" % (disk_user.rio)), style)
            else :
                sheet.write(i, 7, None, style)

            if disk_user.oxford :
                sheet.write(i, 8, float("%.2f" % (disk_user.oxford)), style)
            else :
                sheet.write(i, 8, None, style)

            style = myeasyxf(colour = (i+1)%2, borders='nttm')
            if disk_user.charge :
                sheet.write(i, 9, float("%.2f" % (disk_user.charge)), style)
            else :
                sheet.write(i, 9, None, style)

            i += 1

        style = myeasyxf(colour = (i+1)%2, borders='dmmn')
        sheet.write(i, 0, "Total", style)

        style = myeasyxf(colour = (i+1)%2, borders='dmtn')
        sheet.write(i, 1, float("%.2f" % (self.total_disk_space_from_all_pis)), style)
        sheet.write(i, 2, float("%.2f" % (self.total_disk_charge_from_all_pis)), style)
        sheet.write(i, 3, None, style)
        sheet.write(i, 4, None, style)
        sheet.write(i, 5, float("%.2f" % (self.total_home_usage)), style)
        sheet.write(i, 6, float("%.2f" % (self.total_cork_usage)), style)
        sheet.write(i, 7, float("%.2f" % (self.total_rio_usage)), style)
        sheet.write(i, 8, float("%.2f" % (self.total_oxford_usage)), style)

        style = myeasyxf(colour = (i+1)%2, borders='dmtm')
        sheet.write(i, 9, float("%.2f" % (self.total_charge)), style)
        
        book.save(excel_file)
        return

if __name__ == "__main__" :
    
    disk_usages = DiskUsage()

    disk_usages.create_usage_from_file(input_file = "home", usage = disk_usages.home)
    disk_usages.create_usage_from_file(input_file = "cork", usage = disk_usages.cork)
    disk_usages.create_usage_from_file(input_file = "rio", usage = disk_usages.rio)
    disk_usages.create_usage_from_file(input_file = "oxford", usage = disk_usages.oxford)

    disk_usages.setup_disk_users()
    disk_usages.assign_pi_to_disk_users()
    disk_usages.calculate_total_disk_usage_from_all_pis()
    disk_usages.calculate_total_disk_usage_from_all_users()

    disk_usages.write_to_excel()
