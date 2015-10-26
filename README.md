# Compranet to OCDS
This project processes data from Compranet - a dataset of federal procurement processes from Mexico - and stores it as OCDS records. These records are used to power the dashboards of the [Procurement Analytics](https://github.com/procurement-analytics/procurement-analytics) project.

This purpose of this project is to show what can be done with OCDS records. The mapping of the Compranet fields to OCDS standard is therefore approximate.

## How to use this scripts
The `compranet-ocds.py` script downloads data from the Compranet site, performs cleanup, and transforms it into OCDS records. By default the script will use cached data, but it can also download fresh data from the Compranet site, or use a set of sample data.

```
-d, --download    Force a download of the latest data. If not passed,
                  the script tries to use cached data instead.

-s, --sample      Run the cleanup on a set of sample data. Useful for
                  development.
```

## About the mapping
The script will output one OCDS record package for each month. Since the dashboards are only concerned with the most recent state of a procedure, the `packages` array that usually contains the releases will be empty.

Some notes about the assumptions and caveats of our mapping.

### Tenders, awards and contracts
One of the most determining assumptions in this script, is how the Compranet concepts of Procedimiento, Expediente and Contrato translate into to the OCDS concepts of Tenders, Awards and Contracts.

```
Procedimiento = tender  
\  
 Expediente = ~award  
 \  
  Contrato = contract  
```

This assumption was made based on information from the Compranet team:

> El procedimiento es único, el expediente se integra cuando se concluye un procedimiento y se integran uno o varios contratos.

but also on a further analysis of the procedures with the most records associated.

| Numero procedimiento | Records |
| --- | --- |
| AA-012NAW001-N49-2012 | 940 |
| AA-012NAW001-N60-2012 | 782 |
| AA-012NAW001-N51-2014 | 514 |
| SA-015000999-N93-2014 | 427 |
| AA-012NBG003-N6-2011 | 369 |

Each of these groups of procedures has only one `Numero de Expediente` associated to it, even though they refer to different contracts with different suppliers. The `Codigo Contrato` is always unique.

```
procedimiento -1---n- expediente -1---1- contracto
```

### OCID
The `ocid` is being constructed as follows: `ocds-123456789-0-` + the procedure id. Resulting in IDs such as: `ocds-123456789-0-AA-002000999-I118-2012`.

### Buyer and procuring entity
The dependencia is mapped to the buyer, the unidad de compra to the procuring entity.

### New OCDS fields
To be able to include certain Compranet fields that are necessary for the dashboards, this script adds a couple of new fields to the OCDS:

- `buyer -> type` - the level of government
- `buyer -> abbreviation` - the abbreviation of the buyer
- `tender -> procuringEntity -> abbreviation` abbreviation of the procuring entity
- `tender -> publicationDate` the publication date of the tender
- `award -> suppliers -> sizeSupplier`

### Still to be mapped
The following fields are not mapped to OCDS yet, but are necessary for the procurement dashboards:

- where to store type contract (Service / Obra Publica / etc) Categories seem to generic for the item classification