# Marcus main

An assignment that refactors the main function from Max's code into its own library

### Installation

```
pip install marcus-main
```

### Get started

How to run Max's code using the MarcusMain library

```Python
from marcus_main import MarcusMain

# Instantiate a MarcusMain object and save it to a variable
run = MarcusMain()

# Call the main function. We have to pass the main function a number of arguments that are defined elsewhere in Max's code.
run.main(
    currency_pairs,
    initialize_raw_data_tables,
    initialize_aggregated_tables,
    aggregate_raw_data_tables,
    reset_raw_data_tables,
    ts_to_datetime,
)
```
