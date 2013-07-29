#!/usr/bin/env python


DESCRIPTION = """
imageInsertion.py

Why this script?
Because the docs for transmogrifier are too cool, and
it's clearly beyond me to figure the damn thing out.

These scripts should take advantage of Roc Garbas's rockin'
collective.jsonify package to suck stuff out of the old
Plone 2.5 site via some clever json http call mojo.
(Roc ROCKS, by the way.)
Then, after sucking the data out of the site with
jsonifySucker.py, this script will attempt to shove
the data into the new Plone site.

Yeah, there's probably some muck-sucking transmogrifier
sewerpipline that'd carry this crap directly into the
lavatory that is Plone. I'll believe it when I see
the freaking code and a bullet-list set of instructions
on how it works. The closest thing I found was Regbro's
2009 talk on slideshare. AFAICT, transmogrifier is the
manure from which a migration should eventually emanate.
I'd rather not eat it. Since good stuff spring forth from
collective.jsonify, I'm going to start with that.

Plus, the organization fo the old site is freaky. Yeah,
there's probably some pipelne filter to put stuff
from the old site into something reasonable on the new
site. But, I guess I'm just not that cool.

Oh, and I crammed these into an External method. Joy.

sys.path.append('/web/bga/bga-buildout/scripts'

"""

#import getSite
#from Products.CMFCore.utils import getToolByName
#urltool = getToolByName(portal, 'portal_url')
#portal = urltool.getPortalObject()
#from plone import api
#portal = api.portal.get()

import os
import json
from zope.component.hooks import getSite
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
import transaction
from Products.CMFPlone.utils import _createObjectByType
from dateutil import parser
from DateTime import DateTime
import transaction
from datetime import datetime
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from zope.component import getMultiAdapter


BASEPATH = '/web/bga/sidebarimages/json/'
FILESPATH = '/web/bga/sidebarimages/files/'
BASEURL = 'http://bgavm:8080/goose/goose/images/'

files = [file for file in os.listdir(BASEPATH)]

counter = 0

portal = getSite()

def stickit():
    for img in files:
        jdata = {}
        img = BASEPATH + img

        fd = open(img)
        jdata = json.load(fd)

        _type = jdata['_type']
        #cdate = DateTime(cdate)
        if _type != 'Image':
            print ">> %s is not an Image" % imgid
            continue

        imgid = jdata['id']
        title = jdata['title']
        description = jdata['description']
        cdate = jdata['creation_date']
        cdate = cdate.split('.', -1)[0]
        cdate = parser.parse(cdate)
        #text = jdata['text']
        creators = jdata['creators']
        #import pdb; pdb.set_trace()
        #df = jdata["_datafield_image"]['filename']

        norm = getUtility(IIDNormalizer)
        imgid = norm.normalize(imgid)

        #_path = jdata['_path']
        base = 'images'
        container = portal['sidebar-images']
        print">> creating %s" % imgid
        if imgid in container.contentIds():
            print">> %s already exists. Next..." % imgid
            continue
        _createObjectByType('Image', container, imgid)
        obj = container[imgid]
        # make p_jar on content
        transaction.savepoint(optimistic=True)

        obj.setTitle(title)
        obj.setDescription(description)
        obj.setCreationDate(cdate)
        obj.setEffectiveDate(cdate)
        obj.setModificationDate(cdate)
        obj.setCreators(creators)

        #get the file data
        print ">> adding the %s file data" % imgid
        bin_file = FILESPATH + jdata['_id']
        bin_file = open(bin_file, 'rb')
        # Set the filename
        obj.setImage(bin_file)
        #obj.setFilename(df)
        bin_file.close()

        transaction.commit()

    return "all done"
