import sys, codecs
stop_char = u'\u0003'
with codecs.open('test2.txt', 'w', 'utf-8') as f:
    f.write('ohoeolo' + stop_char + 'x')
