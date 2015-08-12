# Settings - procurement charts
# -*- coding: latin-1 -*-

import chartdata
import domains


#####################################################################
### Generic chart settings

folder_charts = './data/export/charts'

# This is used to date the contracts for the charts on the summary page
main_date_contract = 'FECHA_INICIO'
start_date_charts = '2011-01-01'
end_date_charts = '2015-06-30'

# Currency to use. Either USD / MXN
desired_currency = "MXN"


#####################################################################
### Dashboard settings

# Each chart falls within a particular dimension of procurement
# performance.
dimensions = ['summary', 'timeliness', 'cost-efficiency', 'fairness']

# Each of the dimensions can be analyzed in more detail using 
# comparisons
comparisons = [
  { 
    'id': 'all',
    'compare': None,
    'slices': [
      {'id': 'full', 'label': 'Full dataset'}
    ]
  },
  { 
    'id': 'contract-procedure',
    'compare': 'TIPO_PROCEDIMIENTO',
    'slices': [
      {'id': 'lic-publica', 'label': 'Licitación Pública', 'field': 'Licitacion Publica'},
      {'id': 'adj-directa', 'label': 'Adjudicación Directa Federal', 'field': 'Adjudicacion Directa Federal'},
      {'id': 'invitacion', 'label': 'Invitación a Cuando Menos 3 Personas', 'field': 'Invitacion a Cuando Menos 3 Personas'}
    ]
  },
  { 
    'id': 'size-supplier',
    'compare': 'ESTRATIFICACION_MUC',
    'slices': [
      {'id': 'micro-supplier', 'label': 'Micro', 'field': 'Micro'},
      {'id': 'small-supplier', 'label': 'Small', 'field': 'Pequeña'},
      {'id': 'medium-supplier', 'label': 'Medium', 'field': 'Mediana'},
      {'id': 'big-supplier', 'label': 'No SME', 'field': 'No MIPYME'}
    ]
  }
]


#####################################################################
### Chart configuration

charts = [
  {
    # The dimension this chart belongs to
    'dimension': 'summary',
    # The function used to calculate the data
    'function': chartdata.contracts_time,
    # How domains should be treated across comparisons
    'domain': { 'x': domains.no_update, 'y': domains.min_max }, 
    'meta': {
      'id': 'contracts-time',
      'title': 'Contracts',
      'x': {
        'label': 'Date',
        'domain': []
      },
      'y': {
        'label': 'Contracts',
        'domain': []
      },
      'data': []
    }
  },
  {
    'dimension': 'summary',
    'function': chartdata.amount_time,
    'domain': { 'x': domains.no_update, 'y': domains.min_max },
    'meta': {
      'id': 'amount-time',
      'title': 'Amount',
      'x': {
        'label': 'Date',
        'domain': []
      },
      'y': {
        'label': 'Amount (1000$)',
        'domain': []
      },
      'data': []
    },
  },
  {
    'dimension': 'cost-efficiency',
    'function': chartdata.price_distribution,
    'domain': { 'x': domains.no_update, 'y': domains.min_max },
    'meta': {
      "id": "price-distribution",
      "title": "Price Distribution",
      "x": {
        "domain": [],
        "label": "Price"
      },
      "y": {
        "label": "# of contracts",
        "domain": []
      }
    }
  },
  {
    'dimension': 'cost-efficiency',
    'function': chartdata.price_variation,
    'domain': { 'x':  domains.min_max },
    'meta': {
      'id': 'price-variation',
      'title': 'Price variation',
      'x': {
        'label': 'Price variation',
        'domain': []
      }
    }
  },
  {
    'dimension': 'fairness',
    'function': chartdata.top_contracts,
    'domain': { },
    'meta': {
      "id": "top-contracts",
      "title": "Top 5 contracts",
      "header": [
        "Buyer",
        "Supplier",
        "Amount"
      ]
    }
  },
  {
    'dimension': 'fairness',
    'function': chartdata.relationships,
    'domain': { 'x':  domains.min_max, 'y': domains.min_max, 'r': domains.min_max },
    'meta': {
      "id": "relationship",
      "title": "Relationships",
      'x': {
        'label': 'Amount spent',
        'domain': [],
        'key': 'amount'
      },
      'y': {
        'label': '# of suppliers',
        'domain': [],
        'key': 'suppliers'
      },
      'r': {
        'domain': [],
        'key': 'contracts'
      }
    }
  },
  {
    'dimension': 'timeliness',
    'function': chartdata.average_timeline,
    'domain': { },
    'meta': {
      "id": "average-timeline",
      "title": "Average Timeline",
      'x': {
        'label': 'Days',
        "bands": [
           "1. Bid preparation (publication - start date proposals)",
           "2. Open to bidding (start date proposals - decision)",
           "3. Award time (decision - contract start)"
        ]
      }
    }
  },
  # {
  #   'dimension': 'fairness',
  #   'function': chartdata.concentration_winning,
  #   'domain': { 'x':  domains.min_max, 'y': domains.min_max },
  #   'meta': {
  #     "id": "concentration-winning",
  #     "title": "Concentration of Winning",
  #     'x': {
  #       'label': 'Price',
  #       'domain': [],
  #       'key': 'amount'
  #     },
  #     'y': {
  #       'label': '# of contracts',
  #       'domain': [],
  #       'key': 'contracts'
  #     }
  #   }
  # }
]