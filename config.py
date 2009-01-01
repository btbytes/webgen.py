import os

author = 'Pradeep Gowda' # Default author name. Overridden in individual document
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
input_dir = os.path.join(THIS_DIR, 'input')
#output_dir = os.path.join(THIS_DIR, 'htdocs')
output_dir = '/Users/pradeep/Sites'
template_dir = THIS_DIR
template = os.path.join(template_dir, 'template.html')

### Optional parameters
options = { 'baseurl':'http://localhost/~pradeep', # if not set, relative URLs will be generated
            'sitename':'webgen.py',
            'slogan':'The simplest way to generate static websites',
            'extensions':['txt', 'mkd', 'markdown', 'textile'],
            'format': 'text/x-textile',

        }