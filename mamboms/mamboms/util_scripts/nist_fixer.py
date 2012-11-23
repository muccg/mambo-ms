#!/usr/bin/env python

"""
Fixes the incorrectly wrapped longer CAS NAME lines in a NIST file.

The script has not been writen to be used, it is more of a documentation of what I did with the file.
If it has to be re-run feel free to modify it as required.
"""

def main():
    with open('../docs/nist08_fixed.jca', 'w') as fw:
        prev_line=''
        for line in open('../docs/nist08.jca'):
            if not (line.startswith('##') or line.startswith('  ')):
                fw.write(prev_line.rstrip())
            else:
                fw.write(prev_line)
            prev_line=line
        fw.write(prev_line)

