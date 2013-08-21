#!/bin/env python

from glob import glob
from utility import is_blank_line, list_uniq, check_file_exists
from fullname import hpc_users_with_full_name
        
class HPCPI :
    def __init__(self, line = None) :
        self.owner = None
        self.name = None
        self.members = []
        self.sge_members = []
        self.disk_members = []
        self.cpu = None
        self.disk_space = None
        self.disk_charge = None

        self.department = None
        self.grant = None

        self.troubleshooting = 0.0
        self.consultation = 0.0
        self.shares = 0.0
        self.shares_replication = 0.0

        self.shares_usage = {}
        
        if line :
            tmp = line.split(":")
            self.owner = tmp[0].lstrip()
            self.name = tmp[1].lstrip()
            if len(tmp) == 3 :
                self.members = tmp[2].split()
            if hpc_users_with_full_name().has_key(self.owner) :
                self.members.append(self.owner)
            self.members = list_uniq(self.members)
        return

    def __repr__(self) :
        s = ""
        if self.owner : s += " Owner: %s" % (self.owner)
        if self.name : s += " Name: '%s'" % (self.name)
        if self.department : s += " Department: " + self.department
        if self.grant : s += " Grant: " + self.grant
        if self.shares : s += ' Shares: %.2f' % self.shares
        if self.shares_replication : s += ' Shares-replication: %.2f' % self.shares_replication
        if self.members : s += " Members: " + " ".join(self.members)
        if self.sge_members : s += " SGE-Members: " + " ".join(self.sge_members)
        if self.disk_members : s += " Disk-Members: " + " ".join(self.disk_members)
        return s

_hpc_pis = None

def assign_department() :
    global _hpc_pis
    department_hash_table = '/cork/dicom/department'
    check_file_exists(department_hash_table)
    fin = open(department_hash_table, "r")
    assert fin
    while 1 :
        line = fin.readline()
        if not line : break
        line = line.rstrip()
        if not is_blank_line(line) :
            tmp = line.split(":")
            owner = tmp[0].lstrip()
            department = tmp[1].lstrip()
            if _hpc_pis.has_key(owner) :
                _hpc_pis[owner].department = department
            else :
                print " There is no PI: ", owner
    fin.close()
    return

def assign_troubleshooting() :
    global _hpc_pis
    troubleshooting = 'troubleshooting'
    check_file_exists(troubleshooting)
    fin = open(troubleshooting, 'r')
    assert fin
    while 1 :
        line = fin.readline()
        if not line : break
        line = line.rstrip()
        if not is_blank_line(line) :
            tmp = line.split(":")
            owner = tmp[0].lstrip()
            hours = float(tmp[1].lstrip())
            if _hpc_pis.has_key(owner) :
                _hpc_pis[owner].troubleshooting = hours
            else :
                print " There is no PI: ", owner
    fin.close()
    return

def assign_shares() :
    global _hpc_pis
    shared_files = glob('shares/[a-z]*')

    for f in shared_files :
        check_file_exists(f)
        fin = open(f, 'r')
        assert fin
        while 1 :
            line = fin.readline()
            if not line : break
            line = line.rstrip()
            if not is_blank_line(line) :
                tmp = line.split(":")
                owner = tmp[0].lstrip()
                data = float(tmp[2].lstrip())
                replication =  float(tmp[3].lstrip())
                if _hpc_pis.has_key(owner) :
                    _hpc_pis[owner].shares += data
                    _hpc_pis[owner].shares_replication += replication
                    file_name = f.split('/')[1]
                    _hpc_pis[owner].shares_usage[file_name] = [file_name, tmp[1], data, replication]
                else :
                     print " There is no PI: ", owner
        fin.close()
    return

def hpc_pis() :
    global _hpc_pis
    
    if not _hpc_pis :
        pi_hash_table = '/cork/dicom/pihash2'
        check_file_exists(pi_hash_table)
        
        _hpc_pis = {}
        print " Reading PI has table from " + pi_hash_table
        fin = open(pi_hash_table, "r")
        assert fin
        while 1 :
            line = fin.readline()
            if not line : break
            line = line.rstrip()
            if not is_blank_line(line) :
                hpc_pi = HPCPI(line)
                _hpc_pis[hpc_pi.owner] = hpc_pi
        fin.close()

        assign_department()
        assign_troubleshooting()
        assign_shares()

    return _hpc_pis

if __name__ == "__main__" :

    pis = hpc_pis()

    exit()


    for pi in pis.keys() :
        if pis[pi].shares_usage :
            print pis[pi].shares_usage
            
    

    
