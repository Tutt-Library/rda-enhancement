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
import os
import pymarc
import re
import sys


class PCCMARCtoRDAConversion(BaseMARC21Conversion):

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
                new_a = illus_re.sub("facsimiles", new_a)
                new_a = sound_re.sub("sound", new_a)
                new_a = approx_re.sub("approximately", new_a)
                field_a.delete_subfield('a')
                field_a.add_subfield('a', new_a)


    def remove245EllipsesChangeLatin(self, field245):
        """Method 245 subfield c:  Remove ellipses and change Latin abbreviation
        ("... [et al.]"  becomes "[and others]")"""
        pattern = re.compile("\u2026 \[et al.\]")
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
