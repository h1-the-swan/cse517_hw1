import glob, codecs

fnames = glob.glob('*.txt')
out_str = u''
for fname in fnames:
    print(fname)
    with codecs.open(fname, 'r', 'latin-1') as fopen:
        out_str = out_str + fopen.read()

with codecs.open('aggregated_text.txt', 'w', 'utf-8') as fout:
    fout.write(out_str)
