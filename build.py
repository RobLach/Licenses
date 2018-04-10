import os

from os import path
from string import Template
from configparser import ConfigParser, ExtendedInterpolation


def get_name(p):
    p = path.abspath(p)
    absname, ext = path.splitext(p)
    dir, name = path.split(absname)
    return name


f = open('templates/page-template.html', 'r')
tmpl_page = Template(f.read())
f.close()

f = open('templates/index-template.html', 'r')
tmpl_index = Template(f.read())
f.close()

f = open('templates/index-item-template.html', 'r')
tmpl_index_item = Template(f.read())
f.close()

meta = ConfigParser()
meta._interpolation = ExtendedInterpolation()
meta.read('meta.ini')

index = ''

for root, subdirs, files in os.walk('html'):
    for f in files:
        if not f.endswith('.html') or f == 'index.html':
            continue
        model = dict()

        fo = open('html/' + f, 'r')
        model['license_text'] = fo.read()
        fo.close()

        id = model['license_id'] = get_name(f)
        model['license_name'] = meta[id]['name']

        index += tmpl_index_item.substitute(model)

        fo = open('page/' + get_name(f) + '.html', 'w')
        fo.write(tmpl_page.substitute(model))
        fo.close()

model = dict()
model['items'] = index
index = tmpl_index.substitute(model)

f = open('page/index.html', 'w')
f.write(index)
f.close()

f = open('html/index.html', 'w')
f.write(index)
f.close()
