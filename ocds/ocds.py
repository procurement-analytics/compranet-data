# Compranet OCDS
# -*- coding: latin-1 -*-

import os

import csv
import json
from datetime import date
import pandas as pd

from utils.utils import check_create_folder, clean_folder, get_filename
import settings
import sys


def get_tender_data(record):
  """
  Generate the information about a tender

  :param record:
    
  :type args:

  :returns:
      
  :example:

  """

  r = {
    'ocid': 'ocds-123456789-0-' + record['NUMERO_PROCEDIMIENTO'],
    'buyer': {
      'type': record['GOBIERNO'],
      'abbreviation': record['SIGLAS'],
      'name': record['DEPENDENCIA']
    },
    'tender': {
      'id': record['NUMERO_PROCEDIMIENTO'],
      'procuringEntity': {
        'id': record['CLAVEUC'],
        'name': record['NOMBRE_DE_LA_UC'],
        'contactPoint': { 'name': record['RESPONSABLE'] }
      },
      'tenderPeriod': { 'startDate': record['FECHA_APERTURA_PROPOSICIONES'] },
      'publicationDate': record['PROC_F_PUBLICACION'],
      'eligibilityCriteria': record['CARACTER'],
      'description': record['TIPO_CONTRATACION'],
      'procurementMethod': record['TIPO_PROCEDIMIENTO'],
      'submissionMethod': record['FORMA_PROCEDIMIENTO'],
      'documents': [ {'documentType': 'tenderNotice', 'url': record['ANUNCIO']} ]
    },
    'awards': [],
    'contracts': []
  }

  return r


def get_award_data(record, award_id):
  """
  Get award data for a record

  :param record:
    
  :type record:

  :param award_index:

  :type award_index:

  :returns:
      
  :example:

  """

  award = {
    'id': award_id,
    'title': record['TITULO_EXPEDIENTE'],
    'date': record['EXP_F_FALLO'],
    'suppliers': [ {'name': record['PROVEEDOR_CONTRATISTA'], 'sizeSupplier': record['ESTRATIFICACION_MUC']} ]
  }

  return award


def get_contract_data(record, award_id):
  """
  Get contract data for a record

  :param record:
    
  :type args:

  :returns:
      
  :example:

  """

  contract = {
    'id': record['CODIGO_CONTRATO'],
    'awardID': award_id, 
    'title': record['TITULO_CONTRATO'],
    'period': { 'startDate': record['FECHA_INICIO'], 'endDate': record['FECHA_FIN'] },
    'value': { 'amount': float(record['IMPORTE_CONTRATO']), 'currency': record['MONEDA'] },
    'status': record['ESTATUS_CONTRATO'],
    'dateSigned': record['FECHA_CELEBRACION']
  }

  return contract


def generate_json(df):
  """
  Generate OCDS record packages for each month

  :param df:
    Dataframe with all the contracts
  :type args:
    DataFrame

  :returns:
      
  :example:

  """

  check_create_folder(settings.folder_ocds_json)
  check_create_folder(settings.folder_tmp)
  clean_folder(settings.folder_tmp)

  # Group the Compranet by date
  df['group_date'] = df[settings.grouping_date].convert_objects(convert_dates='coerce')
  grouped_df = df.set_index('group_date').groupby(pd.TimeGrouper(freq='M'))

  # Store the records for each month in a temporary CSV file
  # The JSON files will be generated from these CSV files, which
  # is much more performant than iterating over the rows in pandas
  files = []
  for month, records in grouped_df:
    if not records.empty:
      m = month.strftime("%Y%m%d")
      file_name = os.path.join(settings.folder_tmp, m + '.csv')
      files.append(file_name)
      records.to_csv(file_name, index=False)

  # Loop over each CSV file and create an OCDS record package
  for f in files:

    # Store the package meta-data
    ## ADD MONTH
    package = {
      "uri": os.path.join("http://example.com/" + get_filename(f) + '.json'),
      "publishedDate": get_filename(f),
      "records": [],
      "publisher": {
        "identifier": "100",
        "name": "Compranet"
      },
      "packages": []
    }

    # Read the file and generate the records
    with open(f, 'rb') as infile:
      data = csv.DictReader(infile)

      ocds_records = {}

      for record in data:
        record_id = record['NUMERO_PROCEDIMIENTO']

        # Add the generic tender data for this record,
        # if it's not there already
        if not record_id in ocds_records:
          ocds_records[record_id] = get_tender_data(record)

        # The contract and award data needs to be added for each row

        # OCDS expects a unique ID for every award. NUMERO_EXPEDIENTE is not unique, hence
        # a custom ID
        award_id = str(record['NUMERO_EXPEDIENTE']) + '-' + str(len(ocds_records[record_id]['awards']) + 1)
        
        ocds_records[record_id]['awards'].append(get_award_data(record, award_id))
        ocds_records[record_id]['contracts'].append(get_contract_data(record, award_id))

      for key, value in ocds_records.iteritems():
        package['records'].append(value)

    ofn = os.path.join(settings.folder_ocds_json, get_filename(f) + '.json')
    with open(ofn, 'w') as outfile:
      json.dump(package, outfile)
