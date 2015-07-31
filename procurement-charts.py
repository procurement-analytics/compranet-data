#!/usr/bin/env python
# -*- coding: latin-1 -*-

from datetime import datetime
import json
import numpy as np
import os
import pycurl
import pandas as pd
from utils.utils import check_create_folder, exit, timer

import clean.settings

from charts import settings, chartdata


def slice_df(df, col, field):
  """
  Slice a dataframe

  :param df:
    Pandas dataframe
  :type df:
    Dataframe
  :param col:
    The column name to slice on
  :type col:
    String
  :param field:
    String to slice on
  :type field:
    String

  :returns:
    A sliced dataframe
  """
  try:
    sliced_df = df.groupby(col).get_group(field)
  except KeyError, e:
    print 'The column "%s" doesn\'t contain any "%s"' % (col, field)
    sliced_df = pd.DataFrame()

  return sliced_df


def main():
  """
  Main function - launches the program.
  """

  check_create_folder(settings.folder_charts)

  df = pd.read_csv(os.path.join(clean.settings.folder_cleaned_cache,clean.settings.file_cleaned),parse_dates=True)
  
  # Improve
  df['FECHA_INICIO'] = df['FECHA_INICIO'].convert_objects(convert_dates='coerce')
  df['PROC_F_PUBLICACION'] = df['PROC_F_PUBLICACION'].convert_objects(convert_dates='coerce')
  df['FECHA_APERTURA_PROPOSICIONES'] = df['FECHA_APERTURA_PROPOSICIONES'].convert_objects(convert_dates='coerce')
  df['EXP_F_FALLO'] = df['EXP_F_FALLO'].convert_objects(convert_dates='coerce')


  # Cut every contract that's before a starting date
  start_date = datetime.strptime(settings.start_date_charts,'%Y-%m-%d')
  end_date = datetime.strptime(settings.end_date_charts,'%Y-%m-%d')
  df = df[(df['FECHA_INICIO'] >= start_date) & (df['FECHA_INICIO'] <= end_date)]


  # Generate the summary statistics, independent of comparison or slice
  overview_data = chartdata.generate_overview(df)

  with open(os.path.join(settings.folder_charts, 'general.json'), 'w') as outfile:
    json.dump(overview_data, outfile)


  for dimension in settings.dimensions:
    for comparison in settings.comparisons:

      # Each unique combination of dimension + comparison is a 'lense'
      lense_id = dimension + '--' + comparison['id']
      lense = { 
        'metadata': { 
          'id': lense_id
        },
        'charts': []
      }

      for chart in settings.charts:
        if chart['dimension'] == dimension:
          if chart['function']:
            chart['meta']['data'] = []
       
            previous_slice = False
            d = { }

            # Generate the chart data
            for sl in comparison['slices']:
              sliced_chart = { 'id': sl['id'], 'label': sl['label'] }
              
              # Prep the dataframe, slice it or serve it full
              if comparison['compare']:
                sliced_df = slice_df(df, comparison['compare'], sl['field'])
              else:
                sliced_df = df

              if not sliced_df.empty:
                current_slice = chart['function'](sliced_df)

                # Append the slice's data & meta-data 
                sliced_chart['data'] = current_slice['data']
                chart['meta']['data'].append(sliced_chart)
                
                # Update the domain based on the slice
                for axis, func in chart['domain'].items():
                  if previous_slice:
                    d[axis] = func(d[axis], current_slice['domain'][axis])
                  else:
                    d[axis] = current_slice['domain'][axis]
                  
                previous_slice = True


            # Add the domain to the chart
            for axis, func in chart['domain'].items():
              chart['meta'][axis]['domain'] = d[axis]
            
          # Append the chart data
          lense['charts'].append(chart['meta'])

      file_name = os.path.join(settings.folder_charts,lense_id + '.json')
      with open(file_name, 'w') as outfile:
        json.dump(lense, outfile)


def __main__():

  with timer():
    main()


if __name__ == "__main__":
  try:
    __main__()
  except (KeyboardInterrupt, pycurl.error):
    exit('Received Ctrl + C... Exiting! Bye.', 1)