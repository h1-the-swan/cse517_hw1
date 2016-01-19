def prepare_text(text):
    out = u''
    for i in range(len(text)):
        char = text[i]
        if i > 0:
            out = out + u'q' + char
        out = out + u'o' + char
    return out
