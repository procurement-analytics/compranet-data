# Compranet OCDS
# -*- coding: latin-1 -*-

import os
import numpy

import csv
import pandas as pd

from utils.utils import check_create_folder, get_filename, remove_accents

import settings


def drop(df,col):
  """
  Drops a column from a dataframe 

  :param df:
    Pandas dataframe
  :type args:
    Dataframe
  :param col:
    Column in the dataframe
  :type full:
    String

  :returns:
    Dataframe
  
  """
  df.drop(col, axis=1, inplace=True)

  return df


def proper_string(df,col):
  """
  Titlecase a string

  :param df:
    Pandas dataframe
  :type args:
    Dataframe
  :param col:
    Column in the dataframe
  :type full:
    String

  :returns:
    Dataframe
  
  """
  df[col] = df[col].str.capitalize()

  return df


def currency_convert_dated(curr,amount,date):
  """
  Convert to desired currency using yearly average exchange rate.
  If the year is not specified in the settings file, an average is used.

  :param curr:
    Original currency
  :type args:
    String
  :param amount:
    Amount to be converted
  :type amount:
    Float
  :param date:
    The date/year of the conversion
  :type date:
    String

  :returns:
    (Float) with the converted amount 
  """

  if not curr == settings.desired_currency:
    yr = date[:4]
    xrates = settings.xrate
    if yr in xrates:
      xrate = xrates[yr]
    else:
      xrate = numpy.mean(xrates.values())
    if curr == 'USD':
      amount = round(float(amount) * xrate,2)
    elif curr == 'MXN':
      amount = round(float(amount) / xrate,2)
  return amount


def currency_convert(df,col):
  """
    

  :param df:
    Pandas dataframe
  :type args:
    Dataframe
  :param col:
    Column in the dataframe
  :type full:
    String

  :returns:
    Dataframe
  """

  df[col] = df.apply(lambda row: currency_convert_dated(row['MONEDA'], row[col], row['FECHA_INICIO']), axis=1)

  return df


def str_id(df,col):
  """
  Turn a string with 

  :param df:
    Pandas dataframe
  :type args:
    Dataframe
  :param col:
    Column in the dataframe
  :type col:
    String

  :returns:
    Dataframe
  """

  df[col] = df.apply(lambda row: remove_accents(row[col]), axis=1)

  return df


def map_value(value,field):
  """
  Returns the mapped value

  :param value:
    The field to be mapped
  :type value:
    String
  :param field:
    Column in the dataframe
  :type field:
    String

  :returns:
    String
  """
  try:
    return settings.mapping[field][value]
  except KeyError:
    return value
  

def map_field(df,col):
  """
  Map the values of a field to something else 

  :param df:
    Pandas dataframe
  :type args:
    Dataframe
  :param col:
    Column in the dataframe
  :type col:
    String

  :returns:
    Dataframe
  """

  df[col] = df.apply(lambda row: map_value(row[col],col), axis=1)
  
  return df


# These define the actions to be taken on each of the columns. It is possible
# to specify multiple sequential actions
clean_action = {
  'GOBIERNO': None,
  'SIGLAS': None,
  'DEPENDENCIA': None,
  'CLAVEUC': None,
  'NOMBRE_DE_LA_UC': None,
  'RESPONSABLE': [drop],
  'NUMERO_EXPEDIENTE': None,
  'TITULO_EXPEDIENTE': [proper_string],
  'PLANTILLA_EXPEDIENTE': None,
  'NUMERO_PROCEDIMIENTO': None,
  'EXP_F_FALLO': None,
  'PROC_F_PUBLICACION': None,
  'FECHA_APERTURA_PROPOSICIONES': None,
  'CARACTER': None,
  'TIPO_CONTRATACION': None,
   # in future, map this to OCDS values
  'TIPO_PROCEDIMIENTO': [map_field, str_id],
  'FORMA_PROCEDIMIENTO': None,
  'CODIGO_CONTRATO': None,
  'TITULO_CONTRATO': [proper_string],
  'FECHA_INICIO': None,
  'FECHA_FIN': None,
  'IMPORTE_CONTRATO': [currency_convert],
  'MONEDA': [drop],
  'ESTATUS_CONTRATO': None,
  'ARCHIVADO': None,
  'RAMO': None,
  'CLAVE_PROGRAMA': None,
  'APORTACION_FEDERAL': None,
  'FECHA_CELEBRACION': None,
  'CONTRATO_MARCO': None,
  'COMPRA_CONSOLIDADA': [drop],
  'PLURIANUAL': [drop],
  'CLAVE_CARTERA_SHCP': None,
  'ESTRATIFICACION_MUC': None,
  'PROVEEDOR_CONTRATISTA': [proper_string],
  'ESTRATIFICACION_MPC': None,
  'ESTATUS_EMPRESA': None,
  'CUENTA_ADMINISTRADA_POR': [drop],
  'ANUNCIO': None
}


def clean_csv(source_data):
  """
  Cleans the source data from different files and stores it in one CSV file

  :param source_data:
    List with files to clean
  :type args:
    List

  :returns:
      
  :example:
  
  """
  clean_path = os.path.join(settings.folder_cleaned_cache, settings.file_cleaned)
  first = True

  for source_file in source_data:

    df = pd.read_csv(source_file)

    for key in clean_action:
      if clean_action[key]:
        for action in clean_action[key]:
          df = action(df,key)

    if first:
      # Write the header
      header = df.columns.values.tolist()
      with open(clean_path,'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    df.to_csv(clean_path, mode='a', header=0, index=0)

    first = False