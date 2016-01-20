import sys
text = sys.stdin.read()
text = text.split('\n')
total_hist = u''
for line in text:
    if len(line) == 1 or line[1:3] == u'//':
        total_hist = total_hist + line[0]
sys.stdout.write(total_hist)
