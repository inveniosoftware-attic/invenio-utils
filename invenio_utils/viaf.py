# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from urllib2 import urlopen

from lxml import etree

from invenio_formatter.engine import BibFormatObject

CFG_VIAF_WIKIPEDIA_LINK_BFO_FIELD = "856"
CFG_VIAF_LINK_NAME_LABEL_SUBFIELD = 'n'
CFG_VIAF_WIKIPEDIA_NAME_VALUE_SUBFIELD = 'wikipedia'
CFG_VIAF_WIKIPEDIA_LINK_SUBFIELD = 'a'


def get_wikipedia_link(viaf_id):
    # Query viaf api and parse results
    url = "http://viaf.org/viaf/" + str(viaf_id) + "/viaf.xml"
    string_xml = urlopen(url).read()
    xml = etree.fromstring(str(string_xml))

    # Do an xpath query for all the wikipedia links
    # that can be found for the author and return the first one
    author_wikipedia_id = xml.xpath(
        "/ns2:VIAFCluster/ns2:sources/ns2:source[contains(text(),'WKP')]"
        "/@nsid",
        namespaces={"ns2": "http://viaf.org/viaf/terms#"}
    )
    url_to_wikipedia = None
    if isinstance(author_wikipedia_id, list) and author_wikipedia_id:
        author_wikipedia_id = author_wikipedia_id[0]
        url_to_wikipedia = "http://www.wikipedia.com/wiki/" + \
            author_wikipedia_id
    return url_to_wikipedia


def get_wiki_link_from_record(bfo):
    link = None
    fields = []
    if isinstance(bfo, BibFormatObject):
        fields = bfo.fields(CFG_VIAF_WIKIPEDIA_LINK_BFO_FIELD)
    else:
        fields = bfo.get(CFG_VIAF_WIKIPEDIA_LINK_BFO_FIELD, [])
    for field in fields:
        if isinstance(field, dict):
            if field.get(
                    CFG_VIAF_LINK_NAME_LABEL_SUBFIELD,
                    None) == CFG_VIAF_WIKIPEDIA_NAME_VALUE_SUBFIELD:
                link = field.get(CFG_VIAF_WIKIPEDIA_LINK_SUBFIELD, None)
        else:
            record_dict = {}
            for subfields in field:
                if isinstance(subfields, list):
                    for subfield in subfields:
                        record_dict[subfield[0]] = subfield[1]
            if record_dict.get(
                    CFG_VIAF_LINK_NAME_LABEL_SUBFIELD,
                    None) == CFG_VIAF_WIKIPEDIA_NAME_VALUE_SUBFIELD:
                link = record_dict.get(CFG_VIAF_WIKIPEDIA_LINK_SUBFIELD,
                                       None)
    return link
