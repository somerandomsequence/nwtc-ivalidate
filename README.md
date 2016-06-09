NREL NWTC iValidate
===================

This is a bit of infrastructure code to allow comparison of timeseries from
arbitrary data sources using arbitrary metrics. It is designed to be simple,
and extensible.

To use, simply:

python compare.py config.yaml > output.json

### Configuration

The configuration is given in the YAML format.  An example configuration is provided in config.yaml.

To do a comparison, you'll need at least one basis dataset (called 'left') and one or more datasets to make comparisons to (called 'right'). Each dataset has a path (location), format, and variable. The format string must match one of the classes in the 'inputs' directory.

Currently, only local datasets are supported. Future versions will fetch data over SFTP (i.e., PNNL DAP) and other protocols.

Beyond the datasets, you can list which comparator metrics to compute. Each must correspond to a metric class in the 'metrics' directory.

Preprocessing routines to do downsampling, interpolation, and outlier removal (QA/QC) can be specified with a prepare class in the 'prepare' directory.

You can specify time-based filtering and manipulations (such as trimming and time-windowing) with the time directive.

Finally, you specify the location (in what is assumed to be WGS 84 lat/lon coordinates).

### Adding Metrics

To add a new metric, create a new file in the metrics folder. The filename must match the class name, so if you wanted to write a script that computes MAE, you might call the file metrics/mae.py and the class inside would also be called mae.

The metric class interface is simple, it defines a single method called 'compute' which takes two variables x (left) and y (right). Both are datetime-indexed pandas dataframes.

The function compute() must return a float (single, scalar number).

### Adding Inputs

To add a new data format (or source), create a new file in the inputs folder. As with metrics, the filename must match the class name. So, if you wanted to parse an HDF5 file you might call it hdf5.py and the class name in the file would also be hdf5.

The input class interface expects a constructor that takes the path and variable and a single method called get_ts() which takes a location hash with a lat and lon and returns the timeseries (datetime-indexed Pandas dataframe).

### Adding Preprocessors

To add a new preprocessor or QA/QC routine that operates on each timeseries, take a look in the 'prepare' directory.

### Parallelism

The current implementation is serial, however future versions may exploit local or distributed parallelism by:

  * Loading timeseries data from files (or cache) in parallel
  * Computing metrics for each pair of timeseries in parallel
