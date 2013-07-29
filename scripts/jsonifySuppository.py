#!/usr/bin/env python


DESCRIPTION = """
jsonifySuppository.py

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

BASEPATH = '/web/bga/export/'
FILESPATH = '/web/bga/files/'
BASEURL = 'http://bgavm:8080/goose/goose/bulletin/'
DESTPATH = "bulletins"

portal = getSite()

#def insertion():
#portal = app.bga
files = [file for file in os.listdir(BASEPATH)]

counter = 0

container = portal[DESTPATH]

for file in files:
    jdata = {}
    file = BASEPATH + file

    fd = open(file)
    jdata = json.load(fd)
    _id = jdata['_id']
    _type = jdata['_type']
    title = jdata['title']
    description = jdata['description']
    creators = jdata['creators']
    cdate = jdata['creation_date']
    cdate = cdate.split(' ')[0]
    creation_date = parser.parse(cdate)
    creation_date = DateTime(creation_date)
    #about the file data
    dfile = jdata['_datafield_file']
    dtype = dfile['content_type']
    dfilename = dfile['filename']

    norm = getUtility(IIDNormalizer)
    _id = norm.normalize(_id)
    dfilename = norm.normalize(dfilename)

    _createObjectByType(_type, container, _id)
    obj = container[_id]
    # make p_jar on content
    transaction.savepoint(optimistic=True)

    #get the file data
    bin_file = FILESPATH + jdata['_id']
    bin_file = open(bin_file, 'rb')
    # Set the filename
    obj.setTitle(title)
    obj.setDescription(description)
    obj.setCreationDate(creation_date)
    obj.setCreators(creators)
    obj.setFile(bin_file)
    obj.setFilename(dfilename)
    bin_file.close()
