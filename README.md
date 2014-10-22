# Database Benchmarking

This application is intended to help you benchmark a database of your choice very simply and easily.  Simply follow the specified steps to build a module of your own and then you can see how it stacks up to other similar databases!

The following modules are currently operational:
* Riak DB
* Riak 2.0 DB
* Riak 2.0 DB with highly consistent buckets (NEW!)
* MongoDB (partially, though expect some breaking changes.  For the ansible roles, see my forked repo "ansible-examples/mongodb".  They will soon live in THIS repository!)

## Sample Reports

These reports have already been generated by the developer (your's truly...):
* [Riak 2.0 DB](https://github.com/kmjungersen/DB-Benchmarking/blob/master/generated_reports/RIAK2.report.md)
* [Riak 2.0 DB with highly consistent buckets](https://github.com/kmjungersen/DB-Benchmarking/blob/master/generated_reports/RIAK2_CONSISTENT_.report.md)
* [Riak DB](https://github.com/kmjungersen/DB-Benchmarking/blob/master/generated_reports/RIAK.report.md)
* [MongoDB Replication Set](https://github.com/kmjungersen/DB-Benchmarking/blob/dev/generated_reports/MONGO_REPSET.report.md)
* [MongoDB Sharded Replication Set](https://github.com/kmjungersen/DB-Benchmarking/blob/dev/generated_reports/MONGO_SHARDED_REPSET.report.md)

## Some Nice Features

Some sweet features of using this robust application as opposed to hacking together a quick benchmark
* Ansible roles are included for each module for local testing and deployment
* Easily change module IP and port addresses to run benchmarks on remote deployments, including your development and production servers 
* Robust data analysis gives you an excellent idea of how your database is performing
* Track benchmark progress with the progress bar, while optional verbose output gives you more detailed info on what's going on
* Generate a markdown report to view in a nicely formatted document for showing off to your boss or whomever
* `Invoke` tasks simplify most common tasks for basic usage.
    ```
    invoke help
    ```
    displays the following:
    
    ```
      benchmark             Executes benchmarks with the default settings for a
                            given DB
      deploy                Runs the ansible playbook for a given db
      help                  Returns some basic task information, much of which
                            provided by invoke
      install_ssh_copy_id   Installs ssh_copy_id for mac
      list_mods             Returns a list of existing modules
      vagrant_up            Runs `vagrant up` for the specified module
    ```

## Using the Application

1. Install dependencies from `requirements.txt`.  It's recommended to use a virtual environment.
    ``` bash
    $ cd <path_to_project>/DB-Benchmarking
    $ pip install -r requirements.txt
    ```

2. Deploy the DB
   This procedure is slightly different for every module, so be sure to read the `README` for each one.

3. Run the app!

    ```
    $ python main.py <database_module_name> [options]
    ```

    * General usage information and options:
    ```
    Usage:
        main.py <database> [options]

    Options:
        -h --help           Show this help screen
        -v                  Show verbose output from the application
        -V                  Show REALLY verbose output, including the time
                                from each run

        -c --chaos          Activates CHAOS mode, where reads are taken
                                randomly from the DB instead of sequentially
        -l --list_mods      Outputs a list of available DB modules
        -r --report         Option to generate a report file, which will
                                OVERWRITE any existing reports from the specified
                                DB in the `generated_reports` directory

        --length=<n>        Specify an entry length for reads/writes [default: 10]
        --trials=<n>        Specify the number of reads and writes to make to the
                                DB to collect data on [default: 100]
    ```

## Building a module

If you want to benchmark a DB that isn't already included, build a new module!  Fork the project from dev before making your changes, and then follow the instructions in `CONTRIBUTING.md` to create a new module to use with this application!

Building a new module is extremely easy, so please do so and then submit a PR to share that module with everyone else!
