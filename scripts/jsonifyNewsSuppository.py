#!/usr/bin/env python


DESCRIPTION = """
jsonifyNewsSuppository.py

Why this script?
Because the docs for transmogrifier really don't explain
it clearly enough for me to figure the damn thing out.

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
import transaction
from datetime import datetime

BASEPATH = '/web/bga/news/'
BASEURL = 'http://bgavm:8080/goose/goose/bulletin/'
DESTPATH = "news"

portal = getSite()

#def insertion():
#portal = app.bga
files = [file for file in os.listdir(BASEPATH)]

counter = 0

container = portal[DESTPATH]
def stickit():
    for file in files:
        jdata = {}
        file = BASEPATH + file

        fd = open(file)
        jdata = json.load(fd)
        jdata = jdata[0]
        id = jdata['id']
        title = jdata['title']
        cdate = jdata['creation_date']
        cdate = parser.parse(cdate)
        text = jdata['text']
        #import pdb; pdb.set_trace()

        #cdate = DateTime(cdate)

        norm = getUtility(IIDNormalizer)
        id = norm.normalize(id)

        _createObjectByType('News Item', container, id)
        obj = container[id]
        # make p_jar on content
        transaction.savepoint(optimistic=True)

        #import pdb; pdb.set_trace()
        obj.setText(text)
        obj.setTitle(title)
        obj.setCreationDate(cdate)
        obj.setEffectiveDate(cdate)

        #import pdb; pdb.set_trace()

        obj.setModificationDate(cdate)
        transaction.commit()

    return "all done"
