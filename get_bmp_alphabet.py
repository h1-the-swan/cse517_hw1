# https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane
# and help from http://stackoverflow.com/questions/1477294/generate-random-utf-8-string-in-python
unicode_bmp_range = [ 
        ( 0x0000, 0x0860 ),
        ( 0x089F+1, 0x1C80 ),
        ( 0x1CBF+1, 0x2FE0 ),
        ( 0x2FEF+1, 0xFFFF+1 )
        ]
def get_bmp_alphabet(unicode_bmp_range=unicode_bmp_range):
    """

    :unicode_bmp_range: TODO
    :returns: TODO

    """
    try:
        get_char = unichr
    except NameError:
        get_char = chr

    alphabet = [
            get_char(code_point) for current_range in unicode_bmp_range
                for code_point in range(current_range[0], current_range[1])
        ]
    return alphabet

