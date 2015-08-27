"""-------------------------------------------------------------------------------
# Name:        pcc_conversion
# Purpose:     Implements Program for Cooperative Cataloging's conversion
#              February 25, 2013 recommendations for converting MARC21 records
#              to hybrid RDA records.
#
# Author:      Jeremy Nelson, Anjali Ravunniarath, Jason Stewart
#
# Created:     2014/15/09
# Copyright:   (c) Jeremy Nelson, Colorado College 2014
# Licence:     MIT
#------------------------------------------------------------------------------"""

try:
    import base_converter
except ImportError:
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
        self.convert264()
        self.convert300()
        self.create336()
        self.create337()
        self.create338()
        self.convert500s()

    def convert245(self):
        """Method converts field 245"""
        all245s = self.record.get_fields('245')
        for field245 in all245s:
            self.remove245EllipsesChangeLatin(field245)
            self.remove245GMD(field245)
            new_field245 = self.__format245__(field245)
            self.record.remove_field(field245)
            self.record.add_field(new_field245)

    def convert264(self):
        """Method converts field 260. Changes s.1 to
        place of publication not identified"""
        all264s = self.record.get_fields('264')

        sl_re = re.compile(r"S.l.")
        sn_re = re.compile(r"s\.n\.")

        for field in all264s:
            if len(field.indicators[1].strip()) < 1:
                field.indicators[1] = '1'
            for subfield in field:
                new_subfield = (
                    subfield[0],
                    sl_re.sub(
                        "Place of publication not identified",
                        subfield[1]))
                field.delete_subfield(subfield[0])
                field.add_subfield(new_subfield[0], new_subfield[1])

        for field in all264s:
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

    def create336(self):
        # If 336 already exists return
        field336 = self.record.get_fields('336')
        if len(field336) > 0:
            return
        type_of = self.record.leader[6]
        if type_of in RDA_CONTENT_LOOKUP:
            rda_content_type = RDA_CONTENT_LOOKUP.get(type_of)
            new336 = pymarc.Field(
                '336', 
                indicators=[' ',' '],
                subfields=['a', rda_content_type.get('term'),
                           'b', rda_content_type.get('code'),
                           '2', "rdacontent"])
            self.record.add_field(new336)

    def create337(self):
        # If 337 already exists return
        field337 = self.record.get_fields('337')
        if len(field337) > 0 or not '007' in self.record:
            return
        field007 = self.record['007']
        type_of = field007.data[0]
         
        if type_of in RDA_MEDIA:
            rda_media = RDA_MEDIA.get(type_of)
            new337 = pymarc.Field(
                '337', 
                indicators=[' ',' '],
                subfields=['a', rda_media.get('term'),
                           'b', rda_media.get('code'),
                           '2', "rdamedia"])
            self.record.add_field(new337)

    def create338(self):
        # If 338 already exists return
        field338 = self.record.get_fields('338')
        if len(field338) > 0 or not '007' in self.record:
            return
        field007 = self.record['007']
        type_of = field007.data[1]
        if type_of in RDA_CARRIER_TYPES:
            rda_carrier_type = RDA_CARRIER_TYPES.get(type_of)
            new338 = pymarc.Field(
                '338', 
                indicators=[' ',' '],
                subfields=['a', rda_media.get('term'),
                           'b', rda_media.get('code'),
                           '2', "rdacarrier"])
            self.record.add_field(new338)


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


