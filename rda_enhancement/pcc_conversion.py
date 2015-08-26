"""-------------------------------------------------------------------------------
# Name:        pcc_conversion
# Purpose:     Implements Program for Cooperative Cataloging's conversion
#              February 25, 2013 recommendations for converting MARC21 records
#              to hybrid RDA records.
#
# Author:      Jeremy Nelson, Anjali Ravunniarath
#
# Created:     2014/15/09
# Copyright:   (c) Jeremy Nelson, Colorado College 2014
# Licence:     MIT
#------------------------------------------------------------------------------"""

from . import base_converter

import pymarc
import re

RDA_CARRIER_TYPES = {
    'c': { # 007 - Electronic Resource
        'k': {
            'term': 'computer card',
            'code': 'ck'},
        'b': {
            'term': 'computer chip cartridge',
            'code': 'cb'},
        'z': {
            'term': 'other',
            'code': 'cz'},
        'd': {'term': 'computer disc', 'code': 'cd'},
        'e': {'term': 'computer disc cartridge', 'code': 'ce'},
        'a': {'term': 'computer tape cartridge', 'code': 'ca'},
        'f': {'term': 'computer tape cassette', 'code': 'cf'},
        'r': {'term': 'online resource', 'code': 'cr'},
        'h': {'term': 'computer tape reel', 'code': 'ch'}},
    's': { # 007 - Sound Recording
        't': {'term': 'audiotape reel', 'code': 'st'}, 'g': {'term': 'audio cartridge', 'code': 'sg'}, 'q': {'term': 'audio roll', 'code': 'sq'}, 'z': {'term': 'other', 'code': 'sz'}, 'e': {'term': 'audio cylinder', 'code': 'se'}, 'd': {'term': 'audio disc', 'code': 'sd'}, 's': {'term': 'audiocassette', 'code': 'ss'}, 'i': {'term': 'sound track reel', 'code': 'si'}}}

RDA_CONTENT_LOOKUP = {
    'c': {
        'term': 'tactile notated music',
        'code': 'tcm'},
    'f': {
        'term': 'cartographic three-dimensional form',
        'code': 'crf'},
    'j': {
        'term': 'performed music',
        'code': 'prm'},
    'p': {
        'term': 'other',
        'code': 'xxx'},
    'a': {
        'term': 'text',
        'code': 'txt'}, 'm': {'term': 'computer program ', 'code': 'cop'}, 'k': {'term': 'tactile image ', 'code': 'tci'}, 't': {'term': 'text ', 'code': 'txt'}, 'g': {'term': 'two-dimensional moving image ', 'code': 'tdi'}, 'e': {'term': 'cartographic three-dimensional form ', 'code': 'crf'}, 'd': {'term': 'tactile notated music ', 'code': 'tcm'}, 'r': {'term': 'three-dimensional form ', 'code': 'tdf'}, 'o': {'term': 'other ', 'code': 'xxx'}, 'i': {'term': 'spoken word ', 'code': 'spw'}}

RDA_MEDIA = {
    'c': {
        'term': 'computer',
        'code': 'c'},
    't': {
        'term': 'unmediated',
        'code': 'n'},
    'g': {
        'term': 'projected',
        'code': 'g'},
    'v': {
        'term': 'video',
        'code': 'v'},
    'k': {'term': 'unmediated', 'code': 'n'}, 'h': {'term': 'microform', 'code': 'h'}, 'm': {'term': 'projected', 'code': 'g'}, 'z': {'term': 'other', 'code': 'x'}, 's': {'term': 'audio', 'code': 's'}}

class PCCMARCtoRDAConversion(base_converter.BaseMARC21Conversion):
    """Placeholder for class summary

    Attributes:
        record: pymarc.Record
    """

    pages_re = re.compile(r"p\.")
    volumes_re = re.compile(r"v\.")
    illus_re = re.compile(r"illus|ill\.")
    facsim_re = re.compile(r"facsims.")
    sound_re = re.compile(r"sd.")
    approx_re = re.compile(r"ca\.")

    def __init__(self, marc_record):
        super(PCCMARCtoRDAConversion, self).__init__()
        self.record = marc_record

    def convert(self):
        """Method runs entire PCC recomended
         RDA conversions on its MARC21 record"""
        self.convert245()


    def convert245(self):
        """Method converts field 245"""
        all245s = self.record.get_fields('245')
        for field245 in all245s:
            self.remove245EllipsesChangeLatin(field245)
            self.remove245GMD(field245)
            new_field245 = self.__format245__(field245)
            self.record.remove_field(field245)
            self.record.add_field(new_field245)

    def convert260(self):
        """Method converts field 260. Changes s.1 to
        place of publication not identified"""
        all260s = self.record.get_fields('260')

        sl_re = re.compile(r"S.l.")
        sn_re = re.compile(r"s\.n\.")

        for field in all260s:
            for subfield in field:
                new_subfield = (
                    subfield[0],
                    sl_re.sub(
                        "Place of publication not identified",
                        subfield[1]))
                field.delete_subfield(subfield[0])
                field.add_subfield(new_subfield[0], new_subfield[1])

        for field in all260s:
            for subfield in field:
                new_subfield = (
                    subfield[0],
                    sn_re.sub(
                        "publisher not identified",
                        subfield[1]))
                field.delete_subfield(subfield[0])
                field.add_subfield(new_subfield[0], new_subfield[1])


    def convert300(self):
        """Method converts abbreviations in field 300 to the expanded form"""
        all300s = self.record.get_fields('300')


        for field_a in all300s:
            all_a_subfields = field_a.get_subfields('a')
            for subfield_a in all_a_subfields:
                new_a = PCCMARCtoRDAConversion.pages_re.sub("pages", subfield_a)
                new_a = PCCMARCtoRDAConversion.volumes_re.sub("volumes", new_a)
                new_a = PCCMARCtoRDAConversion.illus_re.sub("illustrations", new_a)
                new_a = PCCMARCtoRDAConversion.facsim_re.sub("facsimiles", new_a)
                new_a = PCCMARCtoRDAConversion.sound_re.sub("sound", new_a)
                new_a = PCCMARCtoRDAConversion.approx_re.sub("approximately", new_a)
                field_a.delete_subfield('a')
                field_a.add_subfield('a', new_a)

        for field_b in all300s:
            all_b_subfields = field_b.get_subfields('b')
            for subfield_b in all_b_subfields:
                new_b = PCCMARCtoRDAConversion.pages_re.sub("pages", subfield_b)
                new_b = PCCMARCtoRDAConversion.volumes_re.sub("volumes", new_b)
                new_b = PCCMARCtoRDAConversion.illus_re.sub("illustrations", new_b)
                new_b = PCCMARCtoRDAConversion.facsim_re.sub("facsimiles", new_b)
                new_b = PCCMARCtoRDAConversion.sound_re.sub("sound", new_b)
                new_b = PCCMARCtoRDAConversion.approx_re.sub("approximately", new_b)
                field_b.delete_subfield('b')
                field_b.add_subfield('b', new_b)



    def remove245EllipsesChangeLatin(self, field245):
        """Method 245 subfield c:  Remove ellipses and change Latin abbreviation
        ("... [et al.]"  becomes "[and others]")"""
        pattern = re.compile(r"\u2026 \[et al.\]")
        c_subfields = field245.get_subfields('c')
        for subfield in c_subfields:
            if pattern.search(subfield):
                pre_string = subfield.split("\u2026")[0]
                field245.delete_subfield(subfield)
                field245.add_subfield('c', '{} [and others]'.format(pre_string))


    def remove245GMD(self, field245):
        """Method removes the General Material Designator (GMD) -- 245
        subfield h  (for example:  $h [electronic resource]) This conversion
        will also be accomplished in the general forma245 of the parent class

        Args:
            field245(pymarc.Field): A 245 field

        """

        field245.delete_subfield('h')

    def create336(self, leader):
        pass

    def convert500s(self):
        """Method to convert all field notes 500 - expanding abbreviations"""
        all500s = self.record.get_fields('500', '501','502','504')
        """There might be other 5XX fields with these abbreviations"""

        intro_re = re.compile(r"introd.")

        for field in all500s:
            for subfield in field:
                new_subfield = (
                    subfield[0],
                    PCCMARCtoRDAConversion.pages_re.sub(
                        "pages",
                        subfield[1]))
                field.delete_subfield(subfield[0])
                field.add_subfield(new_subfield[0], new_subfield[1])

        for field in all500s:
            for subfield in field:
                new_subfield = (
                    subfield[0],
                    intro_re.sub(
                        "Introduction",
                        subfield[1]))
                field.delete_subfield(subfield[0])
                field.add_subfield(new_subfield[0], new_subfield[1])


def main():
    pass

if __name__ == '__main__':
    main()


