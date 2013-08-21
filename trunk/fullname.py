#!/bin/env python

from utility import check_file_exists, is_blank_line

_hpc_users = None

def hpc_users_with_full_name() :
    global _hpc_users
    if not _hpc_users :
        passwd_file = "/etc/passwd"
        check_file_exists(passwd_file)
        print " Reading users from file: " + passwd_file
        _hpc_users = {}
        fin = open(passwd_file, "r")
        assert fin
        while 1 :
            line = fin.readline()
            if not line : break
            line = line.strip()
            if not is_blank_line(line) :
                tmp = line.split(":")
                full_name = tmp[4]
                if is_blank_line(full_name) : full_name = ""
                _hpc_users[tmp[0]] = full_name
        fin.close()

    return _hpc_users
            
if __name__ == "__main__" :
    users = hpc_users_with_full_name()
    users = hpc_users_with_full_name()
    for k in users.keys() :
        print ("%10s  $%s$" % (k, users[k]))


