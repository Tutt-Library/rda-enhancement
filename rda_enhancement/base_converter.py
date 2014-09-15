#-------------------------------------------------------------------------------
# Name:        base_converter
# Purpose:     Provides Basic MARC21 RDA converter for use in other classes
#
# Author:      Jeremy Nelson
#
# Created:     2014/09/15
# Copyright:   (c) Jeremy Nelson, Colorado College 2014
# Licence:     MIT
#-------------------------------------------------------------------------------
from pymarc import Field

class BaseMARC21Conversion(object):

    def __init__(self):
        pass

    def __format245__(self, field245):
        """Method takes a 245 field from a MARC record and returns properly
        formatted subfields. By not copying subfield 'h', performs the first
        conversion PCC recommendation.

        Args:
            field245(pymarc.Field): 245 field

        Returns:
            pymarc.Field
        """
        if field245.tag != '245':
            return
        subfield_a,subfield_c= '',''
        a_subfields = field245.get_subfields('a')
        indicator1,indicator2 = field245.indicators
        if len(a_subfields) > 0:
            subfield_a = a_subfields[0]
            if len(subfield_a) > 0:
                if ['.','\\'].count(subfield_a[-1]) > 0:
                    subfield_a = subfield_a[:-1].strip()
        new245 = Field(tag='245',
                       indicators=[indicator1,indicator2],
                       subfields = ['a', u'{0} '.format(subfield_a)])
        b_subfields = field245.get_subfields('b')
        c_subfields = field245.get_subfields('c')
        n_subfields = field245.get_subfields('n')
        p_subfields = field245.get_subfields('p')
        # Order for 245 subfields are:
        # $a $n $p $b $c
        if len(n_subfields) > 0:
             for subfield_n in n_subfields:
                new245.add_subfield('n', subfield_n)
        if len(p_subfields) > 0:
             for subfield_p in p_subfields:
                new245.add_subfield('p', subfield_p)

        if len(c_subfields) > 0 and len(b_subfields) < 1:
            if 'a' in new245.subfields:
                new245['a'] = '{0} /'.format(new245['a'].strip())
        elif len(b_subfields) > 0:
            if 'a' in new245.subfields:
                new245['a'] = '{0} :'.format(new245['a'].strip())
        if len(b_subfields) > 0:
            for subfield_b in b_subfields:
                new245.add_subfield('b',subfield_b)
        if len(c_subfields) > 0:
            for subfield_c in c_subfields:
                new245.add_subfield('c',subfield_c)
        return new245

def main():
    pass

if __name__ == '__main__':
    main()
