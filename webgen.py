#!/usr/bin/env python
'''
webgen.py

Generate a static website

Assumptions:

 * copying any media files over to the output directory is done by the user.
 * Web site can not have any subdirectories that are named the same as the input directory.
 
'''
import os
import sys
import string
from string import Template
from config import *


# should work even without having any of these.
def dummy(s, **kw):
    print 'Processor missing'
    return s

try: 
    from markdown2 import markdown
except:
    markdown = dummy

try: 
    from textile import textile
except:
    textile = dummy


def ext(s):
    bits = s.split('.')
    if len(bits)>1:
        return bits[1]
    return ''

def process(fname):
    f = open(fname, 'r')
    try:
        head, body = f.read().split('\n\n')
        body
    except:
        print 'Invalid file format : ', fname

def parse(fname):
    f = open(fname, 'r')
    raw = f.read()
    f.close()
    headers = {}
    try:
        (header_lines,body) = raw.split("\n\n", 1)
        for header in header_lines.split("\n"):
            (name, value) = header.split(": ", 1)
            headers[name.lower()] = unicode(value.strip())
        return headers, body
    except:
        raise TypeError, "Invalid page file format."

get_outp = lambda s:'.'.join(s.split('.')[:-1]) + '.html'
           
def get_template(template_dir, template):
    """Takes the directory where templates are located and the template name. Returns a blob containing the template."""
    template = os.path.join(template_dir, template)

    f = open(template, 'r')
    blob = Template(f.read())
    f.close()
    return blob
        
def parse_directory(current_dir, files, output_dir):
    files = [f for f in files if ext(f) in options['extensions']]
    for f in files:
        inp = os.path.join(current_dir,f)
        outp = get_outp(os.path.join(output_dir,f))

        headers, body = parse(inp)

        # Attempt to use the file specified template, if not fall back to default.
        blob = get_template(template_dir, template)
        try:
            blob = get_template(template_dir, headers['template'])
        except:
            pass

        format = options['format']
        try:
            format = headers['content-type']
        except:
            pass
            
        content = {u'text/plain': lambda s: u'<pre>%s</pre>' % s,
                u'text/x-markdown': lambda s: u'%s' % markdown(s),
                u'text/x-textile':  lambda s: u'%s' % textile(s,head_offset=0, validate=0, 
                                    sanitize=1, encoding='utf-8', output='utf-8'),
                u'text/html': lambda s: s}[format](body)
        
        values = headers
        values.update({'content':content})
        values.update(options)
        output = blob.safe_substitute(**values)
        outf = open(outp, 'w')
        outf.write(output)
        outf.close()

def main():
    ### Walks through the input dir creating finding all subdirectories.
    for root, dirs, files in os.walk(input_dir):
        output = root.replace(input_dir, output_dir)
        ### Checks if the directory exists in output and creates it if false.
        if not os.path.isdir(output):
            os.makedirs(output)

        parse_directory(root, files, output)

    
if __name__ == '__main__':
    main()
