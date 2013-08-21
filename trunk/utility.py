#!/bin/env python

from time import localtime, asctime
import sys, re, os
from os import path

blank_line_pattern = re.compile(r'^\s?$')

def die(words) :
    print words
    sys.exit()
    
def is_blank_line(line) :
    if blank_line_pattern.match(line) :
        return True
    else :
        return None

def remove_file(f) :
    if os.path.exists(f) :
        os.remove(f)
    return

def current_time() :
    return asctime(localtime())

def check_file_exists(file_name) :
    if(not path.exists(file_name)) :
        die("File '" + file_name + "' does not exit")
    return

def check_directory_exists(dir_name) :
    if(not path.exists(dir_name)) :
        die("Directory '" + dir_name + "' does not exit")
    return
        
def list_uniq(alist) :
    """
    Fastest order preserving
    """
    set = {}
    return [set.setdefault(e,e) for e in alist if e not in set]

