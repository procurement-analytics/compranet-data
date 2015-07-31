# Compranet OCDS

import glob
import time
import os
import shutil
import sys
import unicodedata

from mixins import VerbosityMixin


class timer(object):
  """
  A timer class.

  :Usage:
    >>> with timer():
  ...     your code
  """
  def __enter__(self):
    self.start = time.time()

  def __exit__(self, type, value, traceback):
    self.end = time.time()
    print 'Time spent : {0:.2f} seconds'.format((self.end - self.start))


def exit(message, code=0):
  """ output a message to stdout and terminates the process.

  :param message:
    Message to be outputed.
  :type message:
    String

  :param code:
    The termination code. Default is 0
  :type code:
    int

  :returns:
    void
  """

  v = VerbosityMixin()
  if code == 0:
    v.output(message, normal=True, arrow=True)
    v.output('Done!', normal=True, arrow=True)
  else:
    v.output(message, normal=True, error=True)
    sys.exit(code)


def check_create_folder(folder):
  """ Check whether a folder exists, if not the folder is created.

  :param folder:
    Path to the folder
  :type folder:
    String

  :returns:
    (String) the path to the folder
  """
  if not os.path.exists(folder):
    os.makedirs(folder)

  return folder


def clean_folder(folder):
  """ Remove the files from a specified folder

  :param folder:
    Path to the folder
  :type folder:
    String

  :returns:
    (String) the path to the folder
  """

  for fn in os.listdir(folder):
    file_path = os.path.join(folder, fn)
    try:
      if os.path.isfile(file_path):
        os.unlink(file_path)
    except Exception, e:
      print e

  return folder
  

def remove_folder(folder):
  """ Remove a folder and its contents

  :param folder:
    Path to the folder
  :type folder:
    String

  """
  shutil.rmtree(folder)


def get_file(path):
    """ Separate the name of the file or folder from the path and return it.
    :param path:
        Path to the folder
    :type path:
        String
    :returns:
        (String) the filename
    :example:
        >>> get_file('/path/to/file.jpg')
        'file.jpg'
    """
    return os.path.basename(path)


def get_filename(path):
  """ Return the filename without extension.
  :param path:
      Path to the folder
  :type path:
      String
  :returns:
      (String) the filename without extension
  :example:
      >>> get_filename('/path/to/file.jpg')
      'file'
  """
  return os.path.splitext(get_file(path))[0]
  

def list_files(pattern,path=True):
  """ Return a list with files in a folder matching a pattern

  :param pattern:
    Path + file name. May contain wildcards in the filename
  :type folder_path:
    String
  :param path:
    By default, file names are returned with path. When set to False, only
    file name is returned.
  :type path:
    Boolean

  :returns:
    (List) with filenames, with or without path
  :example:
    >>> ['./sample/Contratos2013.csv', './sample/Contratos2010.csv']
    >>> ['Contratos2013.csv', 'Contratos2010.csv']

  """
  # Use glob to support wildcards on the filename.
  results = glob.glob(pattern)

  if results:
    files_found = []
    for result in results:
      # Check if at least one of the results is a file
      if os.path.isfile(result):
        if path:
          files_found.append(result)
        else: 
          files_found.append(os.path.basename(result))
  
    return files_found


def remove_accents(input_str):
  if type(input_str) is str:
    
    # Remove accents
    # Expects unicode string, not bytestring
    encoding = "utf-8"
    unicode_string = input_str.decode(encoding)

    nkfd_form = unicodedata.normalize('NFKD', unicode_string)
    return  u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

  else:
    return None