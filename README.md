# Procurement Analytics data
This project processes data from Compranet - a dataset of federal procurement processes from Mexico - and prepares it to be used by [Procurement Analytics](https://github.com/procurement-analytics/procurement-analytics)

This repository contains two scripts that are usually run in sequence:

1. `prep-compranet.py`
Fetch the latest data and perform cleanup on the CSV files
2. `procurement-charts.py`
Use the CSV files from `prep-compranet.py` to build the JSON with aggregate data that powers the dashboards

## 1. Process Compranet data
This script downloads data from the Compranet site and performs cleanup. By default the script will use cached data, but can also download fresh data from the Compranet site, or use a set of sample data.

```
-d, --download    Force a download of the latest data. If not passed,
                  the script tries to use cached data instead.

-s, --sample      Run the cleanup on a set of sample data. Useful for
                  development.
```

## 2. Prepare the aggregate data
This can be run on the CSV files produced by `prep-compranet.py`.

# OCDS support
There are plans to have the first script output the data in OCDS format. The `procurement-charts.py` would then read the OCDS records and potentially be used for other datasets that follow the OCDS standard.