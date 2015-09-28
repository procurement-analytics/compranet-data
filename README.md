# Procurement Analytics data
This project processes data from Compranet - a dataset of federal procurement processes from Mexico - and stores it as OCDS records. These records are used to power the dashboards of the [Procurement Analytics](https://github.com/procurement-analytics/procurement-analytics) project.

## Process Compranet data
The `compranet-ocds.py` script downloads data from the Compranet site, performs cleanup, and transforms it into OCDS records. By default the script will use cached data, but it can also download fresh data from the Compranet site, or use a set of sample data.

```
-d, --download    Force a download of the latest data. If not passed,
                  the script tries to use cached data instead.

-s, --sample      Run the cleanup on a set of sample data. Useful for
                  development.
```

The script will output 1 json file per OCDS record.