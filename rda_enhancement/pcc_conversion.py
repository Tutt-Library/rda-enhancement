#-------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------
from base_converter import BaseMARC21Conversion

import pymarc
import re


class PCCMARCtoRDAConversion(BaseMARC21Conversion):
    """Placeholder for class summary

    Attributes:
        record: pymarc.Record
    """

    def __init__(self, marc_record):
        super(PCCMARCtoRDAConversion, self).__init__()
        self.record = marc_record

    def convert(self):
        "Method runs entire PCC recomended RDA conversions on its MARC21 record"
        self.convert245()


    def convert245(self):
        all245s = self.record.get_fields('245')
        for field245 in all245s:
            self.remove245EllipsesChangeLatin(field245)
            self.remove245GMD(field245)
            new_field245 = self.__format245__(field245)
            self.record.remove_field(field245)
            self.record.add_field(new_field245)

    def convert260(self):
        all260s = self.record.get_fields('260')

        s1_re = re.compile(r"S.1.")
        sn_re = re.compile(r"s.n.")

        for all_fields in all260s:
            for all_subfields in all_fields:
                subfields = all_fields.get_subfields('all_subfields')
                for subfield in subfields:
                    new_field = s1_re.sub("Place of publication not identified", subfield)
                    new_field = sn_re.sub("publisher not identified", new_field)
                    all_fields.delete_subfield('all_subfields')
                    all_fields.add_subfield('all_subfields', new_field)


    def convert300(self):
        all300s = self.record.get_fields('300')

        preface_pages_re = re.compile(r"(\w+), (\w+) p+")
        pages_re = re.compile(r"p.")
        volumes_re = re.compile(r"v.")
        illus_re = re.compile(r"illus|ill.")
        facsim_re = re.compile(r"facsims.")
        sound_re = re.compile(r"sd.")
        approx_re = re.compile(r"ca.")

        for field_a in all300s:
            all_a_subfields = field_a.get_subfields('a')
            for subfield_a in all_a_subfields:
                new_a = pages_re.sub("pages", subfield_a)
                new_a = volumes_re.sub("volumes", new_a)
                new_a = illus_re.sub("illustrations", new_a)
                new_a = facsim_re.sub("facsimiles", new_a)
                new_a = sound_re.sub("sound", new_a)
                new_a = approx_re.sub("approximately", new_a)
                field_a.delete_subfield('a')
                field_a.add_subfield('a', new_a)

        for field_b in all300s:
            all_b_subfields = field_b.get_subfields('b')
            for subfield_b in all_b_subfields:
                new_b = pages_re.sub("pages", subfield_b)
                new_b = volumes_re.sub("volumes", new_b)
                new_b = illus_re.sub("illustrations", new_b)
                new_b = facsim_re.sub("facsimiles", new_b)
                new_b = sound_re.sub("sound", new_b)
                new_b = approx_re.sub("approximately", new_b)
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




def main():
    pass

if __name__ == '__main__':
    main()
