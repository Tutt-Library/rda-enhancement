#-------------------------------------------------------------------------------
# Name:        pcc_conversion
# Purpose:     Implements Program for Cooperative Cataloging's conversion
#              February 25, 2013 recommendations for converting MARC21 records
#              to hybrid RDA records.
#
# Author:      Jeremy Nelson
#
# Created:     2014/15/09
# Copyright:   (c) Jeremy Nelson, Colorado College 2014
# Licence:     MIT
#-------------------------------------------------------------------------------
import BaseMARC21Conversion
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
            self.__format245__(field245)

    def convert300(self):
        preface_pages_re = re.compile(r"(\w+), (\w+) p+")
        illus_re = re.compile(r"illus|ill.")




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
        subfield h  (for example:  $h [electronic resource])"""
        field245.delete_subfield('h')




def main():
    pass

if __name__ == '__main__':
    main()
