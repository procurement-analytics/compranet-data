# Settings - prep Compranet
# -*- coding: latin-1 -*-


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


#####################################################################
### Mapping

# This is a generic mapper, mapping values from a particular column
# in the dataset

mapping = {
            "TIPO_PROCEDIMIENTO": {
              "Licitación Pública con OSD": "open",
              "Licitación Publica Estatal": "open",
              "Licitación Pública": "open",
              "Invitación a Cuando Menos 3 Personas": "selective",
              "Adjudicación Directa Federal": "limited"
            },
            "FORMA_PROCEDIMIENTO": {
              "Electrónica": "electronicSubmission",
              "Presencial": "inPerson",
              "Presencial (Estatal)": "inPerson",
              # mixed is a custom category, which is allowed for this field
              "Mixta": "mixed",
              "Mixta (Estatal)": "mixed"
            },
            "ESTATUS_CONTRATO": {
              "Activo": "active",
              "Terminado": "terminated",
              "Expirado": "terminated"
            }
          }