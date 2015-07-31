# Settings - prep Compranet


#####################################################################
### About Compranet

# Base url of the compranet source data
compranet_base_url = 'http://upcp.funcionpublica.gob.mx/descargas/'
fn_prefix = 'Contratos'
years = ['2010_2012', '2013', '2014', '2015']
fn_extension = '.zip'


#####################################################################
### Project structure

folder_full_cache = '.cache/source'
folder_sample_data = './data/sample'
folder_cleaned_cache = '.cache/cleaned'
file_cleaned = 'compranet-cleaned.csv'


#####################################################################
### Currency settings

# Currency to use. Either USD / MXN
desired_currency = "MXN"

# Official exchange rate (LCU per US$, period average)
# Source 2010 - 2014: http://data.worldbank.org
# Source 2015: Google Finance (June 19, 2015)
xrate = {
  "2015": 15.3,
  "2014": 13.29,
  "2013": 12.77,
  "2012": 13.17,
  "2011": 12.42,
  "2010": 12.64
}