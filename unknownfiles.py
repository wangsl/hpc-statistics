#!/bin/env python

from utility import check_file_exists, is_blank_line

_unknown_files = None

def unknown_files() :
    global _unknown_files

    if not _unknown_files :
        unknown_files_hash_table = '/cork/dicom/fshash'
        check_file_exists(unknown_files_hash_table)
        _unknown_files = {}
        
        print " Reading file hash table from " + unknown_files_hash_table
        fin = open(unknown_files_hash_table, "r")
        assert fin
        while 1 :
            line = fin.readline()
            if not line : break
            line = line.rstrip()
            if not is_blank_line(line) :
                tmp = line.split(":")
                assert len(tmp) == 2
                _unknown_files[tmp[0]] = tmp[1].lstrip()
        fin.close()

    return _unknown_files

if __name__ == "__main__" :
    print unknown_files()

    
