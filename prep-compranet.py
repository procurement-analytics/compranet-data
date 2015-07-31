#!/usr/bin/env python

# Compranet OCDS
# A tool to process Mexican procurement data from Compranet

import argparse
import unicodecsv
import os
import pycurl
import textwrap
import xlrd
import zipfile

from homura import download

from clean import clean, settings

from utils.mixins import VerbosityMixin
from utils.utils import check_create_folder, clean_folder, exit, get_filename, timer, list_files, remove_folder


DESCRIPTION = """A tool to process Mexican procurement data from Compranet for use 
  in the Procurement Analytics project.

  Commands:
    prep-compranet.py [-s, --sample | -d, --download]

    optional arguments:
      -s, --sample        Use sample data.

      -d, --download      Force a download of the latest data. By default, the
                          the script tries to use cached data instead.
"""


def args_options():
  """ Generates an argument parser.
  :returns:
    Parser object
  """

  parser = argparse.ArgumentParser(prog='python prep-compranet.py',
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description=textwrap.dedent(DESCRIPTION))

  group = parser.add_mutually_exclusive_group()
  group.add_argument('-s', '--sample', action='store_true',
                      help='Use sample data.')
  group.add_argument('-d', '--download', action='store_true', 
                      help='Download fresh data. This will clear the cache.')

  return parser


def download_compranet(years):
  """
  Download Compranet data for a list of years, unzip the files and convert 
  the XLS to CSV

  :param years:
    The years for which to download data
  :type years:
    List

  :returns:

  :example:

  """
  
  tmp_folder = os.path.join(settings.folder_full_cache, 'tmp')
  check_create_folder(tmp_folder)

  for year in years:
    file_name = os.path.join(settings.fn_prefix + year + settings.fn_extension)
    src_url = settings.compranet_base_url + file_name

    print "Downloading %s" % file_name
    download(url=src_url, path=tmp_folder) 

    file_path = os.path.join(tmp_folder, file_name)
    with zipfile.ZipFile(file_path, 'r') as myzip:
      myzip.extractall(tmp_folder)

  pattern = os.path.join(tmp_folder, '*.xls*')

  for src_file in list_files(pattern):
    csv_path = os.path.join(settings.folder_full_cache, get_filename(src_file) + '.csv')
    wb = xlrd.open_workbook(src_file)
    sheet = wb.sheet_by_index(0)

    with open(csv_path, 'w') as csvfile:
      writer = unicodecsv.writer(csvfile, encoding='utf-8')
      for rownum in xrange(sheet.nrows):
        writer.writerow(sheet.row_values(rownum))

  remove_folder(tmp_folder)


def main(args):
  """
  Main function - launches the program.
  :param args:
    The Parser arguments
  :type args:
    Parser object
  :returns:
    List  
  :example:
    ["Downloading files from the Compranet site."]
  """
  
  if args:

    if args.sample:
      source_folder = settings.folder_sample_data
    
    else:
      # Use cached versions of the source data in csv format
      source_folder = settings.folder_full_cache      
      check_create_folder(source_folder)
      
      if args.download:
        clean_folder(source_folder)
        download_compranet(settings.years)
        
    # Check if there are CSV files in the sample folder
    pattern = os.path.join(source_folder, '*.csv')
    source_data = list_files(pattern)

    if source_data:
      print "About to clean the data"
      clean.clean_csv(source_data)
    else:
      return["No source data found. Make sure there is at least one CSV file in " + source_folder, 1]

    return["Prepared and cleaned the files from the Compranet site.",0]


def __main__():

  global parser
  parser = args_options()
  args = parser.parse_args()
  with timer():
    exit(*main(args))


if __name__ == "__main__":
  try:
    __main__()
  except (KeyboardInterrupt, pycurl.error):
    exit('Received Ctrl + C... Exiting! Bye.', 1)