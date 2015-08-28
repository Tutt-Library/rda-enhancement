__author__ = "Jeremy Nelson"

import argparse
import datetime
import logging
import pymarc
import sys
from rda_enhancement import pcc_conversion

logging.basicConfig(
    filename='error.log', 
    format='%(asctime)s %(message)s',
    level=logging.ERROR)

def convert(input_mrc_filename, output_mrc_filename):
    """Function takes an input MARC21 file, runs the PCC RDA conversion
    on each record, and saves the resulting converted RDA MARC records
    as the output filepath.

    Args:
        input_mrc_filename -- File path to input MARC file

    Returns:
         output_mrc_filename -- File path for converted RDA MARC records
    """
    input_reader = pymarc.MARCReader(open(input_mrc_filename,
                                          "rb"),
                                     to_unicode=True)
    output_writer = pymarc.MARCWriter(open(output_mrc_filename,
                                           "bw+"))
    start = datetime.datetime.now()
    print("Converting {} to RDA at {}".format(
        input_mrc_filename, 
        start.isoformat()))
    for i,rec in enumerate(input_reader):
        converter = pcc_conversion.PCCMARCtoRDAConversion(rec)
        if not i%10 and i > 0:
            print(".", end='')
        if not i%100:
            print(i, end='')
        try:
            converter.convert()
            new_record = pymarc.Record()
            new_record.leader = rec.leader
            for field in sorted(converter.record.fields,
                        key=lambda x: x.tag):
                new_record.add_field(field)
            output_writer.write(new_record)
        except:
            logging.error(
                "Failed to convert record number={}, error={}".format(
                    i,
                    sys.exc_info()[0]))
            continue
    output_writer.close()
    end = datetime.datetime.now()
    print("Finished Converting {} records to RDA at {} total={} minutes".format(
        i,
        end.isoformat(),
        (end-start).seconds / 60.0))     
        
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input', 
        help='File path and name for input MARC21 records for RDA conversion')
    parser.add_argument(
        '--output', 
        help='File path and name for converted RDA MARC21 records')
    args = parser.parse_args()
    convert(args.input, args.output)


