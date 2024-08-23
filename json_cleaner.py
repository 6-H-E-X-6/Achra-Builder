import re

def sanitize(input):
    no_colorcode = re.sub(r'\[.+?\]', '', input)
    return re.sub('  +', '', no_colorcode)
