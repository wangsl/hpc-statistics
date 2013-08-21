#!/bin/env python

from fullname import hpc_users_with_full_name
from hpcpi import hpc_pis
from utility import die, check_file_exists
import re, os

month_pattern = re.compile(r'^[0-9][0-9]-[0-9][0-9]$')
date_pattern = re.compile(r'^[0-9][0-9]-[0-9][0-9]-[0-9][0-9]$')

class _SGEUser :
    def __init__(self, line = None) :
        self.owner = None
        self.wall_clock = None
        self.utime = None
        self.stime = None
        self.cpu = None
        self.memory = None
        self.IO = None
        self.IOW = None
        
        self.name = None
        self.pi = None
        
        if line :
            tmp = line.split()
            assert len(tmp) == 8
            self.owner = tmp[0]
            self.wall_clock = float(tmp[1])
            self.utime = float(tmp[2])
            self.stime = float(tmp[3])
            self.cpu = float(tmp[4])
            self.memory = float(tmp[5])
            self.io = float(tmp[6])
            self.iow = float(tmp[7])

            # assign name
            users_with_full_name = hpc_users_with_full_name()
            if users_with_full_name.has_key(self.owner) :
                self.name = hpc_users_with_full_name()[self.owner]
            else :
                print " ** There is no full name for '" + self.owner + "'"
                self.name = ""

            # assign PI
            _hpc_pis = hpc_pis()
            found_pi = 0
            for pi_owner in _hpc_pis.keys() :
                if found_pi : break
                pi = _hpc_pis[pi_owner]
                for member in pi.members :
                    if member == self.owner :
                        self.pi = pi.owner
                        found_pi = 1
                        break
            
        return

    def add(self, other) :
        assert isinstance(other, _SGEUser)
        assert self.owner == other.owner
        assert self.pi == other.pi
        self.wall_clock += other.wall_clock
        self.utime += other.utime
        self.stime += other.stime
        self.cpu += other.cpu
        self.memory += other.memory
        self.io += other.io
        self.iow += other.iow
        return

    def __repr__(self) :
        s = ""
        if self.owner : s += " Owner: %s" % (self.owner)
        if self.name : s += " Name: %s" % (self.name)
        if self.pi : s += " PI: %s" % (self.pi)
        if self.cpu : s += " CPU: %.3f" % (self.cpu)
        return s

class SGEUsers :

    def __init__(self) :
        self.sge_users = {}
        return

    def create_sge_users_from_command(self, begin, end) :

        _begin_date= None
        _end_date = None

        begin_time = None
        end_time = None
        
        if month_pattern.match(begin) :
            _begin_date = begin + "-01"
        elif date_pattern.match(begin) :
            _begin_date = begin
        else :
            die("'" + begin + "' is not in correct date format, YY-MM-DD, YY-MM")

        if month_pattern.match(end) :
            _end_date = end + "-01"
        elif date_pattern.match(end) :
            _end_date = end
        else :
            die("'" + end + "' is not in correct date format, YY-MM-DD, YY-MM")

        begin_time = "".join(_begin_date.split("-")) + "0000"
        end_time = "".join(_end_date.split("-")) + "0000"
            
        qacct_command = "qacct -o -b " + begin_time + " -e " + end_time + " 2>&1 | egrep -v '^error: |^OWNER |^====' | grep '^[a-z]'"
        
        print " SGE command: ", qacct_command
        
        qacct_output = os.popen(qacct_command)
        while 1 :
            line = qacct_output.readline()
            if not line : break
            line = line.rstrip()
            sge_user = _SGEUser(line)
            if not self.sge_users.has_key(sge_user.owner) :
                self.sge_users[sge_user.owner] = sge_user
            else :
                self.sge_users[sge_user.owner].add(sge_user)

        qacct_output.close()
        return

    def create_sge_users_from_file(self, sge_file) :
        check_file_exists(sge_file)
        print " Reading from file: " + sge_file
        fin = open(sge_file, "r")
        assert fin
        while 1 :
            line = fin.readline()
            if not line : break
            line = line.strip()
            sge_user = _SGEUser(line)
            if not self.sge_users.has_key(sge_user.owner) :
                self.sge_users[sge_user.owner] = sge_user
            else :
                self.sge_users[sge_user.owner].add(sge_user)
        
        fin.close()
        return

def sge_users(begin = None, end = None, sge_qacct_output_file = None) :
    _sge_users = SGEUsers()
    if begin and end :
        _sge_users.create_sge_users_from_command(begin = begin, end = end)
    elif sge_qacct_output_file :
        if isinstance(sge_qacct_output_file, str) :
            _sge_users.create_sge_users_from_file(sge_file = sge_qacct_output_file)
        elif isinstance(sge_qacct_output_file, list) :
            for sge_file in sge_qacct_output_file: 
                _sge_users.create_sge_users_from_file(sge_file = sge_file)
    else :
        die(" argument error")
    return _sge_users.sge_users


if __name__ == "__main__" :

    import os

    
    _sge_users = sge_users(sge_qacct_output_file = ["chaim.usage", "albert.usage"])
    for u in _sge_users.keys() :
        print _sge_users[u]
        
    
    

    
        
