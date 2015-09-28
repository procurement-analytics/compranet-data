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

  # Group the Compranet contracts by procedimiento. Each procedimiento outputs a JSON file
  grouped_df = df.groupby('NUMERO_PROCEDIMIENTO')

  for procedure, records in grouped_df:
    file_name = os.path.join(settings.folder_ocds_json, str(procedure) + '.json')

    with open(file_name,'w') as outfile:
      # Store all data of the procedure
      # Since this is common for all procedures, fetch the data for the first result
      r = {
        'buyer': {
          'type': records.iloc[0]['GOBIERNO'],
          'abbreviation': records.iloc[0]['SIGLAS'],
          'name': records.iloc[0]['DEPENDENCIA']
        },
        'tender': {
          'id': procedure,
          'procuringEntity': {
            'id': records.iloc[0]['CLAVEUC'],
            'name': records.iloc[0]['NOMBRE_DE_LA_UC'],
            'contactPoint': { 'name': records.iloc[0]['RESPONSABLE'] }
          },
          'tenderPeriod': { 'startDate': records.iloc[0]['FECHA_APERTURA_PROPOSICIONES'] },
          'eligibilityCriteria': records.iloc[0]['CARACTER'],
          'description': records.iloc[0]['TIPO_CONTRATACION'],
          'procurementMethod': records.iloc[0]['TIPO_PROCEDIMIENTO'],
          'submissionMethod': records.iloc[0]['FORMA_PROCEDIMIENTO'],
          'documents': [ {'documentType': 'tenderNotice', 'url': records.iloc[0]['ANUNCIO']} ]
        },
        'awards': [],
        'contracts': []
      }

      icontract = 1
      for i, row in records.iterrows():
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

      json.dump(r, outfile)