# BenchmarkDB

Benchmark database performance!  

Master: [![Build Status](https://travis-ci.org/kmjungersen/BenchmarkDB.svg?branch=master)](https://travis-ci.org/kmjungersen/BenchmarkDB)
Develop: [![Build Status](https://travis-ci.org/kmjungersen/BenchmarkDB.svg?branch=develop)](https://travis-ci.org/kmjungersen/BenchmarkDB)

The following database modules are currently operational:
* Riak 1.x DB
* Riak 2.0 DB
* Riak 2.0 DB with highly consistent buckets
* MongoDB (Sharded replication set)
* Cassandra
* PostgreSQL (semi-sharded cluster - see module [README](benchmarkdb/postgreSQLdb/README.md))

## Sample Reports

These reports have already been generated by the developer (your's truly...):
Recently updated with graphs:

* [Riak 1.x DB - 50000 reads/writes](published_reports/riakdb/RIAK-standard-50000trials/RIAK-standard-50000trials.md)
* [Riak 2.0 DB - 50000 reads/writes](published_reports/riak2db/RIAK2-standard-50000trials/RIAK2-standard-50000trials.md)
* [Riak 2.0 DB with high consistency - 50000 reads/writes](published_reports/riak2db/RIAK2-consistent-50000trials/RIAK2-consistent-50000trials.md)
* [MongoDB Sharded Replication Set - 50000 reads/writes](published_reports/mongodb/MONGO-ShardedCluster-50000trials/MONGO-ShardedCluster-50000trials.md)
* [PostgreSQL Semi-Sharded Cluster - 50000 reads/writes](published_reports/postgresql/POSTGRESQL-SemiSharded-50000trials/POSTGRESQL-SemiSharded-50000trials.md)

## Some Nice Features

Some sweet features of using this robust application as opposed to hacking together a quick benchmark
* Generate a markdown report to view in a nicely formatted document, complete with a flask app to view them in the browser
* Benchmark in an isolated environment, or point the app to a staging box to get more realistic benchmarks
* Data Analysis with pandas allows you to handle a large number of benchmark trials (I've tried up to 100k)
* MatPlotLib graphs of data for quick visualization
* Ansible or docker deployment for each module, enabling local or remote deployment and testing
* Easily customize application to run benchmarks on remote or local deployments 
* `Invoke` tasks simplify basic usage.
    
    ```
      Available tasks:

          benchmark             Executes benchmarks with the default settings for a
                                given DB
          help                  Returns some basic task information, much of which
                                provided by invoke
          list_mods             Returns a list of existing modules
          module_requirements   Installs requirements for a specific module
          requirements          Pip installs all requirements, and if db arg is passed, the
                                requirements for that module as well
    ```

## Using the Application

1. Install dependencies in a virtual environment using invoke (`$ pip install invoke` if need be).
    ``` bash
    $ invoke requirements
    ```

2. Install the desired module.

   Although this will soon be automated, for now see the `README` for each module. If you're using a DB that's already deployed, simply update `local.py` for the intended module.

3. Run the app!

    ```
    $ cd BenchmarkDB
    $ python main.py <database_module_name> [options]
    ```
    
    Examples:
    
    ``` bash
    # Benchmark 3000 reads and writes of mongo separately, with randomly ordered reads
    $ python main.py mongodb -c --split --trials=3000
    
    # Benchmark Riak 2.0 with 10000 reads and writes, each with two 1000 character fields, 
    # and then generate a CSV file of the raw data
    $ python main.py riak2db --csv --trials=10000 --length=1000
    
    # Run the application in debug mode, which generates a Normal (Gaussian) data set for 
    # analysis and debugging
    $ python main.py --debug
    ```

    * General usage information and options: `$ python main.py -h`:
    ``` bash
    Usage:
        main.py <database> [options]
        main.py --debug [options]
        main.py <database> <report_title> [options]

    Options:
        -h --help           Show this help screen
        -v                  Show verbose output from the application
        -V                  Show REALLY verbose output, including the time
                                from each run
        -s                  Sleep mode (experimental) - sleeps for 1/20 (s)
                                between each read and write
        -c --chaos          Activates CHAOS mode, where reads are taken
                                randomly from the DB instead of sequentially
        -l --list           Outputs a list of available DB modules
        --csv               Records unaltered read and write data to a CSV file
                                for your own analysis
        --no-report         Option to disable the creation of the report file
        --no-split          Alternate between reads and writes instead of all
                                writes before reads
        --debug             Generates a random dataset instead of actually
                                connecting to a DB
        --length=<n>        Specify an entry length for reads/writes
                                [default: 10]
        --trials=<n>        Specify the number of reads and writes to make to
                                the DB to collect data on [default: 1000]
    ```

## Building a module

If you want to benchmark a DB that isn't already included, build a new module!  Fork the project from dev before making your changes, and then follow the instructions in `CONTRIBUTING.md` to create a new module to use with this application!

Building a new module is extremely easy, so please do so and then submit a PR to share that module with everyone else!
