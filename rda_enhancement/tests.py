#-------------------------------------------------------------------------------
# Name:        tests
# Purpose:     Unit tests for RDA Enhancement Project
#
# Author:      Jeremy Nelson
#
# Created:     2014/09/15/
# Copyright:   (c) Jeremy Nelson, Colorado College 2014
# Licence:     MIT
#-------------------------------------------------------------------------------
__author__ = "Jeremy Nelson"

import copy
import pymarc
import unittest
from base_converter import BaseMARC21Conversion
from pcc_conversion import PCCMARCtoRDAConversion

FIELD245_1 = pymarc.Field(
            tag='245',
            indicators=['1', '0'],
            subfields=[
                'a', 'Basic Concepts of Probability and Statistics in the Law',
                'h', '[electronic resource] /',
                'c', 'by Michael O. Finkelstein.'])

REC_1 = b'01760nam a22003735i 4500001001800000003000900018005001700027007001500044008004100059020003700100024003500137050001700172072001500189072002300204082001200227100003200239245010800271264005400379300004500433336002600478337002600504338003600530347002400566520051300590650002201103650002201125650003101147710003401178773002001212776003601232856004801268912001401316950005601330\x1e978-1-4302-5981-7\x1eDE-He213\x1e20140807044706.0\x1ecr nn 008mamaa\x1e140807s2014    xxu|    s    |||| 0|eng d\x1e  \x1fa9781430259817\x1f9978-1-4302-5981-7\x1e7 \x1fa10.1007/978-1-4302-5981-7\x1f2doi\x1e 4\x1faQA75.5-76.95\x1e 7\x1faUY\x1f2bicssc\x1e 7\x1faCOM014000\x1f2bisacsh\x1e04\x1fa004\x1f223\x1e1 \x1faWojcieszyn, Filip.\x1feauthor.\x1e10\x1faASP.NET Web API 2 Recipes\x1fh[electronic resource] :\x1fbA Problem Solution Approach /\x1fcby Filip Wojcieszyn.\x1e 1\x1faBerkeley, CA :\x1fbApress :\x1fbImprint: Apress,\x1fc2014.\x1e  \x1faXXVI, 368 p. 17 illus.\x1fbonline resource.\x1e  \x1fatext\x1fbtxt\x1f2rdacontent\x1e  \x1facomputer\x1fbc\x1f2rdamedia\x1e  \x1faonline resource\x1fbcr\x1f2rdacarrier\x1e  \x1fatext file\x1fbPDF\x1f2rda\x1e  \x1faASP.NET Web API Recipes provides you with the code to solve a full range of Web API problems and question marks that you might face when developing line-of-business applications. ASP.NET Web API Recipes gives you an in-depth explanation for each of these scenarios and shows you how to use Web API with a vast array of .NET application development tools and external libraries, to solve common business problems. Find out how you can build custom web services with ASP.NET Web API more efficiently than ever.\x1e 0\x1faComputer science.\x1e14\x1faComputer Science.\x1e24\x1faComputer Science, general.\x1e2 \x1faSpringerLink (Online service)\x1e0 \x1ftSpringer eBooks\x1e08\x1fiPrinted edition:\x1fz9781430259800\x1e40\x1fuhttp://dx.doi.org/10.1007/978-1-4302-5981-7\x1e  \x1faZDB-2-CWD\x1e  \x1faProfessional and Applied Computing (Springer-12059)\x1e\x1d'

class BaseMARC21ConversionTests(unittest.TestCase):

    def setUp(self):
        self.field245_1 = copy.deepcopy(FIELD245_1)
        self.record_1 = pymarc.Record()
        self.record_1.decode_marc(REC_1)
        self.marc21_converter = BaseMARC21Conversion()

    def test_format245_forward_slash(self):
        new_field245 = self.marc21_converter.__format245__(self.field245_1)
        self.assertEqual(
            "=245  10$aBasic Concepts of Probability and Statistics in the Law /$cby Michael O. Finkelstein.",
            str(new_field245))

    def test_format245_colon(self):
        new_field245 = self.marc21_converter.__format245__(self.record_1['245'])
        self.assertEqual(
            "=245  10$aASP.NET Web API 2 Recipes :$bA Problem Solution Approach /$cby Filip Wojcieszyn.",
            str(new_field245))


    def tearDown(self):
        pass


class PCCMARCtoRDAConversionTests(unittest.TestCase):

    def setUp(self):
        self.field245_1 = copy.deepcopy(FIELD245_1)
        self.record_1 = pymarc.Record()
        self.record_1.decode_marc(REC_1)
        self.converter = PCCMARCtoRDAConversion(self.record_1)

    def test_convert245(self):
        self.converter.convert245()
        self.assertEqual(
            "=245  10$aASP.NET Web API 2 Recipes :$bA Problem Solution Approach /$cby Filip Wojcieszyn.",
            str(self.record_1['245']))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()