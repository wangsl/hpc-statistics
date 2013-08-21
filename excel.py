#!/bin/env python

import xlwt
from xlwt import easyxf
from xlwt import Workbook, Font, XFStyle, easyxf, Style, Pattern
from utility import die

_global_font = None
_global_alignment = None
_global_pattern_black = None

_bold_blue_font_ = None
_bold_black_font_ = None
_bold_black_underline_font_ = None
_black_font_ = None

_left_alignment_ = None
_right_alignment_ = None
_center_alignment_ = None

_global_patterns = {}
_global_borders = {}
_myeasyxf = {}
_myeasyxf2 = {}

def _border_type(type) :
    if type == 'n' :
        return xlwt.Borders.NO_LINE
    elif type == 't' :
        return xlwt.Borders.THIN
    elif type == 'm' :
        return xlwt.Borders.MEDIUM
    elif type == 'd' :
        return xlwt.Borders.DOUBLE
    else :
        die(" argument error: " + str(type))
    return

def global_borders(type) :
    global _global_borders
    if not _global_borders.has_key(type) :
        borders = xlwt.Borders()
        types = list(type)
        assert len(types) == 4
        borders.top = _border_type(types[0])
        borders.bottom = _border_type(types[1])
        borders.left = _border_type(types[2])
        borders.right = _border_type(types[3])
        _global_borders[type] = borders
        
    return _global_borders[type]
    
def global_font() :
    global _global_font 
    if not _global_font :
        _global_font = Font()
        _global_font.name = 'Arial'
        _global_font.height = 200
    return _global_font 

def global_alignment() :
    global _global_alignment
    if not _global_alignment :
        _global_alignment = xlwt.Alignment()
        _global_alignment.horz = xlwt.Alignment.HORZ_RIGHT
        _global_alignment.vert = xlwt.Alignment.VERT_CENTER
    return _global_alignment

def global_patterns(colour) :
    global _global_patterns
    itype = str(colour)
    if not _global_patterns.has_key(itype) :
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        if colour == 0 :
            pattern.pattern_fore_colour = 1
        elif colour == 1 :
            pattern.pattern_fore_colour = 22
        else :
            die("argument error: " + itype)
        _global_patterns[itype] = pattern
    return _global_patterns[itype]

def myeasyxf(colour, borders) :
    global _myeasyxf
    itype = str(colour) + borders
    if not _myeasyxf.has_key(itype) :
        style = easyxf() 
        style.font = global_font()
        style.alignment = global_alignment()
        style.pattern = global_patterns(colour=colour)
        style.borders = global_borders(type=borders)
        _myeasyxf[itype] = style
    return _myeasyxf[itype]

def bold_blue_font() :
    global _bold_blue_font_
    if not _bold_blue_font_ :
        _bold_blue_font_ = Font()
        _bold_blue_font_.name = 'Calibri'
        _bold_blue_font_.colour_index = 0x12
        _bold_blue_font_.height = 320
        _bold_blue_font_.bold = True
    return _bold_blue_font_

def bold_black_font() :
    global _bold_black_font_
    if not _bold_black_font_ :
        _bold_black_font_ = Font()
        _bold_black_font_.name = 'Calibri'
        _bold_black_font_.height = 240
        _bold_black_font_.bold = True
    return _bold_black_font_

def bold_black_underline_font() :
    global _bold_black_underline_font_
    if not _bold_black_underline_font_ :
        _bold_black_underline_font_ = Font()
        _bold_black_underline_font_.name = 'Calibri'
        _bold_black_underline_font_.height = 240
        _bold_black_underline_font_.bold = True
        _bold_black_underline_font_.underline = True
    return _bold_black_underline_font_


def black_font() :
    global _black_font_
    if not _black_font_ :
        _black_font_ = Font()
        _black_font_.name = 'Calibri'
        _black_font_.height = 240
    return _black_font_

def left_alignment() :
    global _left_alignment_
    if not _left_alignment_ :
        _left_alignment_ = xlwt.Alignment()
        _left_alignment_.horz = xlwt.Alignment.HORZ_LEFT
        _left_alignment_.vert = xlwt.Alignment.VERT_CENTER
    return _left_alignment_

def right_alignment() :
    global _right_alignment_
    if not _right_alignment_ :
        _right_alignment_ = xlwt.Alignment()
        _right_alignment_.horz = xlwt.Alignment.HORZ_RIGHT
        _right_alignment_.vert = xlwt.Alignment.VERT_CENTER
    return _right_alignment_

def center_alignment() :
    global _center_alignment_
    if not _center_alignment_ :
        _center_alignment_ = xlwt.Alignment()
        _center_alignment_.horz = xlwt.Alignment.HORZ_CENTER
        _center_alignment_.vert = xlwt.Alignment.VERT_CENTER
    return _center_alignment_

def myeasyxf2(colour = None, borders = None, font = 'black', alignment = 'left',
              num_format_str = None) :
    global _myeasyxf2

    font = font
    
    itype = ""

    if colour :
        itype += str(colour)
    else :
        itype += "-"

    if borders :
        itype += borders
    else :
        itype += "-"

    if font :
        itype += font
    else :
        itype += "-"

    if alignment :
        itype += alignment
    else :
        itype += "-"

    if num_format_str :
        itype += num_format_str
    else :
        itype += "-"

    if not _myeasyxf2.has_key(itype) :
        style = None

        if num_format_str :
            style = easyxf(num_format_str=num_format_str)
        else :
            style = easyxf()

        if colour :
            style.pattern = global_patterns(colour=colour)

        if borders :
            style.borders = global_borders(type=borders)

        if font == "bold_blue" :
            style.font = bold_blue_font()
        elif font == "bold_black" :
            style.font = bold_black_font()
        elif font == "bold_black_underline" :
            style.font = bold_black_underline_font()
        elif font == "black" :
            style.font = black_font()
        else :
            die("unkown font type: " + font)

        if alignment == "left" :
            style.alignment = left_alignment()
        elif alignment == "right" :
            style.alignment = right_alignment()
        elif alignment == "center" :
            style.alignment = center_alignment()
        else :
            die("unknown alignment: " + alignment)

        _myeasyxf2[itype] = style

    return _myeasyxf2[itype]
        
    
    itype = str(colour) + borders
    if not _myeasyxf.has_key(itype) :
        style = easyxf() 
        style.font = global_font()
        style.alignment = global_alignment()
        style.pattern = global_patterns(colour=colour)
        style.borders = global_borders(type=borders)
        _myeasyxf[itype] = style
    return _myeasyxf[itype]

if __name__ == "__main__" :

    print global_borders('ntmd')
    print global_borders('ntmd')
    print global_borders('nntn')
    print global_borders('nntn')

    print 
    print myeasyxf(colour=0, borders='ntmd')
    print myeasyxf(colour=0, borders='ntmd')
    print myeasyxf(colour=1, borders='ntmd')
    print myeasyxf(colour=1, borders='ntmd')
