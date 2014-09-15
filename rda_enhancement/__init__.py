__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__author__ = "Jeremy Nelson"
__license__ = 'MIT'
__copyright__ = '(c) 2014 by Jeremy Nelson, Colorado College'

from pymarc import Field

class BaseMARC21Conversion(object):

    def __init__(self):
        pass

    def __format245__(self, field245):
        """Method takes a 245 field from a MARC record and returns properly
        formatted subfields

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
            new245.add_subfield('h','{0} / '.format(subfield_h_val))
        elif len(b_subfields) > 0:
            new245.add_subfield('h','{0} : '.format(subfield_h_val))
        else:
            new245.add_subfield('h',subfield_h_val)
        if len(b_subfields) > 0:
            for subfield_b in b_subfields:
                new245.add_subfield('b',subfield_b)
        if len(c_subfields) > 0:
            for subfield_c in c_subfields:
                new245.add_subfield('c',subfield_c)
        return new245