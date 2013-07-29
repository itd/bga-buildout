#!/usr/bin/env python


DESCRIPTION = """
jsonifySucker.py

Why this script?
Because the docs for transmogrifier are too cool, and
it's clearly beyond me to figure the damn thing out.

These scripts should take advantage of Roc Garbas's rockin'
collective.jsonify package to suck stuff out of the old
Plone 2.5 site via some clever json http call mojo.
(Roc ROCKS, by the way.)
Then, after making the call, this script will write-out
that content to disk.

I'll import the crap bit-by-bit into a Plone 4.3.2 site.

Yeah, there's probably some muck-sucking transmogrifier
sewerpipline that'd carry this crap directly into the
lavatory that is Plone. I'll believe it when I see
the freaking code and a bullet-list set of instructions
on how it works. The closest thing I found was Regbro's
2009 talk on slideshare. AFAICT, transmogrifier is the
manure from which a migration should eventually emanate.
I'd rather not eat it. Since good stuff spring forth from
collective.jsonify, I'm going to start with that.
"""

import os
import requests
import json
import time

BASEPATH = '/web/bga/sidebarimages/json/'
FILESPATH = '/web/bga/sidebarimages/files/'
BASEURL = 'http://bgavm:8080/goose/goose/images/core/sidebar-images/'

for i in [FILESPATH, BASEPATH]:
    if not os.path.isdir(i):
        os.makedirs(i)


things = requests.get(BASEURL+'get_children', auth=('admin', 'admin'))
things = things.text[2:-2]
things = things.split('", "')

COUNTER = 0


def suck():
    for objid in things:
        global COUNTER
        COUNTER += 1
        targpath = '%s/%s.json.%s' % (BASEPATH, COUNTER, objid)
        item = requests.get(BASEURL+objid+'/get_item', auth=('admin', 'admin'))
        f = open(targpath, "wb")
        f.write(item.text)
        print "- wrote %s to %s " % (objid, targpath)

        try:
            jdata = json.loads(item.text)
        except ValueError:
            import pdb; pdb.set_trace()
            continue

        # import pdb; pdb.set_trace()

        if jdata['_type'] in ['File', 'Image']:
            fid = jdata['_id']
            f_path = FILESPATH + fid
            datafile = requests.get(BASEURL+fid, auth=('admin', 'admin'))
            f = open(f_path, "wb")
            f.write(datafile.content)
            f.close()
            print "- wrote %s " % (f_path)
            print 'waiting 5 seconds'
            time.sleep(5)

        print ">> all done!"


# item.title
# item.id
# item.creation_date
# item.getText()
