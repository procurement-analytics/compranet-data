# Compranet OCDS
# -*- coding: latin-1 -*-

import os

import csv
import json
from datetime import date
import pandas as pd

from utils.utils import check_create_folder
import settings

def generate_json(df):
  """
  Generate JSON files in OCDS format. One per procedimiento

  :param df:
    Dataframe with all the contracts
  :type args:
    DataFrame

  :returns:
      
  :example:

  """

  check_create_folder(settings.folder_ocds_json)

  # Group the Compranet by date
  df['group_date'] = df[settings.grouping_date].convert_objects(convert_dates='coerce')
  grouped_df = df.set_index('group_date').groupby(pd.TimeGrouper(freq='M'))

  for month, records in grouped_df:
    # Group the Compranet contracts by procedimiento. Each procedimiento outputs a JSON file
    grouped_records = records.groupby('NUMERO_PROCEDIMIENTO')

    package = {
      "uri": "http://example.com/" + str(month),
      "publishedDate": str(month),
      "records": [],
      "publisher": {
        "identifier": "100",
        "name": "Compranet"
      },
      "packages": []
    }

    for procedure, data in grouped_records:
      
      # Store all data of the procedure
      # Since this is common for all procedures, fetch the data for the first result
      r = {
        'ocid': 'ocds-123456789-0-' + str(procedure),
        'buyer': {
          'type': data.iloc[0]['GOBIERNO'],
          'abbreviation': data.iloc[0]['SIGLAS'],
          'name': data.iloc[0]['DEPENDENCIA']
        },
        'tender': {
          'id': procedure,
          'procuringEntity': {
            'id': data.iloc[0]['CLAVEUC'],
            'name': data.iloc[0]['NOMBRE_DE_LA_UC'],
            'contactPoint': { 'name': data.iloc[0]['RESPONSABLE'] }
          },
          'tenderPeriod': { 'startDate': data.iloc[0]['FECHA_APERTURA_PROPOSICIONES'] },
          'eligibilityCriteria': data.iloc[0]['CARACTER'],
          'description': data.iloc[0]['TIPO_CONTRATACION'],
          'procurementMethod': data.iloc[0]['TIPO_PROCEDIMIENTO'],
          'submissionMethod': data.iloc[0]['FORMA_PROCEDIMIENTO'],
          'documents': [ {'documentType': 'tenderNotice', 'url': data.iloc[0]['ANUNCIO']} ]
        },
        'awards': [],
        'contracts': []
      }

      icontract = 1
      for i, row in data.iterrows():
        # Each row contains data about an expediente & contract

        # OCDS expects a unique ID for every award. NUMERO_EXPEDIENTE is not unique, hence
        # a custom ID
        award_id = str(row['NUMERO_EXPEDIENTE']) + '-' + str(icontract)

        award = {
          'id': award_id,
          'title': row['TITULO_EXPEDIENTE'],
          'date': row['EXP_F_FALLO'],
          'suppliers': [ {'name': row['PROVEEDOR_CONTRATISTA'], 'sizeSupplier': row['ESTRATIFICACION_MUC']} ]
        }
        r['awards'].append(award)

        contract = {
          'id': row['CODIGO_CONTRATO'],
          'awardID': award_id, 
          'title': row['TITULO_CONTRATO'],
          'period': { 'startDate': row['FECHA_INICIO'], 'endDate': row['FECHA_FIN'] },
          'value': { 'amount': float(row['IMPORTE_CONTRATO']), 'currency': row['MONEDA'] },
          'status': row['ESTATUS_CONTRATO'],
          'dateSigned': row['FECHA_CELEBRACION']
        }
        r['contracts'].append(contract)

        icontract += 1

      package['records'].append(r)

    m = month.strftime("%Y%m%d")
    file_name = os.path.join(settings.folder_ocds_json, m + '.json')
    with open(file_name,'w') as outfile:
      json.dump(package, outfile)
