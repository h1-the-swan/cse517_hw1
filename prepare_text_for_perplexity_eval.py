import argparse, sys, codecs, time
parser = argparse.ArgumentParser(description='prepare text to alternately query and observe for the language model')
parser.add_argument('-f', '--fname', type=str, help='filename to be used as input')
parser.add_argument('-o', '--outf', type=str, help='filename to be used as output (if not specified, output to stdout)')
parser.add_argument('--stdin', help='use stdin instead of input file', action='store_true')
args = parser.parse_args()
fname = args.fname
outf = args.outf

def prepare_text(text):
    out = u''
    for i in range(len(text)):
        char = text[i]
        if i > 0:
            out = out + u'q' + char
        out = out + u'o' + char
    return out

def output(s):
    if outf:
        print(outf)
        with codecs.open(outf, 'w', 'utf-8') as f:
            f.write(s)
    else:
        sys.stdout.write(s)

if __name__ == "__main__":
    if fname and args.stdin:
        print("error: can't specify both input file and --stdin")
        sys.exit(1)
    if fname:
        with codecs.open(fname, 'r', 'utf-8') as f:
            text = f.read()
        out = prepare_text(text)
        output(out)
    if args.stdin:
        text = sys.stdin.read()
        text = unicode(text)
        text = text.strip()
        out = prepare_text(text)
        output(out)
