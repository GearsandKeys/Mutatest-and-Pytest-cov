# Mutatest and Mutation Testing
## What is Mutation Testing?
Are you confident in your tests? 

Try out `mutatest` and see if your tests will detect small modifications (mutations) in the code. 
Surviving mutations represent subtle changes that are undetectable by your tests. 
These mutants are potential modifications in source code that continuous integration checks would miss.
## Getting Started
Install from PyPI:

`$ pip install mutatest`

Install from conda-forge:

`$ conda install -c conda-forge mutatest`

## [FAQ](https://mutatest.readthedocs.io/en/latest/install.html#motivation-and-faqs)
### Can I use mutatest in CICD?
Yes, though because of the slow nature of running your test suite multiple times it is not something you would run across your entire codebase on every commit. 
Mutatest includes an option to [raise survivor exceptions](https://mutatest.readthedocs.io/en/latest/commandline.html#raising-exceptions-for-survivor-tolerances) based on a tolerance level e.g., you may tolerate up to 2 surviving mutants (you set the threshold) out of 20 with specific pieces of your source code. Mutatest is most useful as a diagnostic tool to determine weak spots in your overall test structure.

Tested on Linux, Windows, and MacOS with Azure pipelines.

### Are there differences in running with Python 3.7 vs. Python 3.8?
New in version 2.0.0: Support for Python 3.8

New in version 3.0.0: Multiprocessing parallelization in Python 3.8
More [here!](https://mutatest.readthedocs.io/en/latest/install.html#are-there-differences-in-running-with-python-3-7-vs-python-3-8)

### Limitations
Since mutatest operates on the local `__pycache__` it is a serial execution process. This means it will take as long as running your test suite in series for the number of operations. You should try to find the combination of test commands, source specifiers, and exclusions that generate meaningful diagnostics. For example, if you have 600 tests, running mutatest over the entire test suite may take some time. A better strategy would be:

- Select a subset of your tests and run pytest with coverage to see the covered percentage per source file.
- Run mutatest with the same pytest command passed in with -t and generating a coverage file. Use -s to pick the source file of interest to restrict the sample space, or use -e to exclude files if you want to target multiple files.

If you kill the mutatest process before the trials complete you may end up with partially mutated `__pycache__` files. If this happens the best fix is to remove the `__pycache__` directories and let them rebuild automatically the next time your package is imported (for instance, by re-running your test suite).

The mutation status is based on the return code of the test suite e.g. 0 for success, 1 for failure. 

## Running Mutatest
### Specific File locally
`mutatest -s <path_to_python_file> -t "pytest" -r 314` (Pytest is the default)

## All files locally
`mutatest -s . -r 314`

## Fast Mode
5 trials, in sd mode (break on first survivor)

`mutatest -s . -n 5 -m sd -r 314`

### Selecting a Running Mode
`mutatest` has different running modes to make trials faster. The running modes determine what will happen after a mutation trial. For example, you can choose to stop further mutations at a location as soon as a survivor is detected. The different running mode choices are:

### Running Modes
- f: full mode, run all possible combinations (slowest but most thorough).

- s: break on first SURVIVOR per mutated location e.g. if there is a single surviving mutation at a location move to the next location without further testing. This is the default mode.

- d: break on the first DETECTION per mutated location e.g. if there is a detected mutation on at a location move to the next one.

- sd: break on the first SURVIVOR or DETECTION (fastest, and least thorough).

The API for mutatest.controller.run_mutation_trials offers finer control over the run method beyond the CLI.

### Controlling Randomization and trial number:
`mutatest` uses random sampling of all source candidate locations and of potential mutations to substitute at a location. You can set a random seed for repeatable trials using the `--rseed` argument. The `--nlocations` argument controls the size of the sample of locations to mutate. If it exceeds the number of candidate locations then the full set of candidate locations is used.

```
mutatest --nlocations 5 --rseed 314

# using shorthand arguments
mutatest -n 5 -r 314
```

### Setting the output location
By default, mutatest will only create CLI output to stdout. You can set path location using the --output argument for a written RST report of the mutation trial results.
```
$ mutatest --output path/to/my_custom_file.rst

# using shorthand arguments
$ mutatest -o path/to/my_custom_file.rst
```

## Raising Exceptions for Survivor Tolerances
By default, `mutatest` will only display output and not raise any final exceptions if there are survivors in the trial results. You can set a tolerance number using the `--exception` or `-x`argument that will raise an exception if that number if met or exceeded for the count of survivors after the trials. This argument is included for use in automated running of `mutatest` e.g. as a stage in continuous integration.

When combined with the random seed and category selection you can have targeted stages for important sections of code where you want a low count of surviving mutations enforced.

```
mutatest --exception 5

# using shorthand arguments
 mutatest -x 5
```

## Parallelization
The --parallel argument can be used if you are running with Python 3.8 to enable multiprocessing of mutation trials. This argument has no effect if you are running Python 3.7. Parallelism is achieved by creating parallel cache directories in a .mutatest_cache/ folder in the current working directory. Unique folders for each trial are created and the subprocess command sets PYTHONPYCACHEPREFIX per trial. These sub-folders, and the top level .mutatest_cache/ directory, are removed when the trials are complete. Multiprocessing uses all CPUs detected by os.cpu_count() in the pool.

The parallel cache adds some IO overhead to the trial process. You will get the most benefit from multiprocessing if you are running a longer test suite or a high number of trials. All trials get an additional 10 seconds added to the maximum timeout calculation as a buffer for gathering results. If you notice excessive false positive timeouts try running without parallelization.

`mutatest --parallel`

## Using a Config File
The contents of an example mutatest.ini or entry in setup.cfg. [See an example here](https://mutatest.readthedocs.io/en/latest/commandline.html#example-config-file).

## Combining with Coverage Tests
[Documentation](https://pytest-cov.readthedocs.io/en/latest/)


## Resources
- [Mutations](https://mutatest.readthedocs.io/en/latest/mutants.html)
- [Mutatest Documentation](https://mutatest.readthedocs.io/en/latest/index.html)
- [Mutatest Github](https://github.com/EvanKepner/mutatest)

# Coverage Testing
Test coverage is defined as a metric in Software Testing that measures the amount of testing performed by a set of test. It will include gathering information about which parts of a program are executed when running the test suite to determine which branches of conditional statements have been taken.

In simple terms, it is a technique to ensure that your tests are testing your code or how much of your code you exercised by running the test.

## pytest-cov
`pytest-cov` is a plugin produces coverage reports. Compared to just using coverage run this plugin does some extras:

- Subprocess support: you can fork or run stuff in a subprocess and will get covered without any fuss.
- Xdist support: you can use all of pytest-xdist’s features and still get coverage.
- Consistent pytest behavior. If you run coverage run -m pytest you will have slightly different sys.path (CWD will be in it, unlike when running pytest).
- All features offered by the coverage package should work, either through pytest-cov’s command line options or through coverage’s config file.

[Documentation](https://pytest-cov.readthedocs.io/en/latest/)

## Usage
`pytest --cov=<project_name> <test_directory>`

So for this repo you would use:

`pytest --cov=app tests/`

Then you will get a report like:
```
4 passed in 0.15s 
PS C:\Users\nathan.gearke\Local Work\mutpy-testing> pytest --cov=app
test session starts 
platform win32 -- Python 3.10.1, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: C:\Users\nathan.gearke\Local Work\mutpy-testing
plugins: anyio-3.5.0, cov-3.0.0, mock-3.6.1
collected 4 items

tests\test_calculator.py ....                                                                                                                                                           [100%]

---------- coverage: platform win32, python 3.10.1-final-0 -----------
Name                Stmts   Miss  Cover
---------------------------------------
app\__init__.py         1      0   100%
app\calculator.py       9      0   100%
---------------------------------------
TOTAL                  10      0   100%
```
## Creating a Data File
The data file is erased at the beginning of testing to ensure clean data for each test run. If you need to combine the coverage of several test runs you can use the `--cov-append` option to append this coverage data to coverage data from previous test runs.

The data file is left at the end of testing so that it is possible to use normal coverage tools to examine it.

## Some Cool Stuff!
`pytest --cov-report term-missing --cov=app tests/`

Reports line numbers!

`pytest --cov-report term:skip-covered --cov=myproj tests/`

Skips covered tests!

## Output
These three report options output to files without showing anything on the terminal:
```
pytest --cov-report html
        --cov-report xml
        --cov-report annotate
        --cov=spp tests/
```

The output location for each of these reports can be specified. The output location for the XML report is a file. Where as the output location for the HTML and annotated source code reports are directories:
```
pytest --cov-report html:cov_html
        --cov-report xml:cov.xml
        --cov-report annotate:cov_annotate
        --cov=app tests/
```
The final report option can also suppress printing to the terminal:

`pytest --cov-report= --cov=app tests/`

This mode can be especially useful on continuous integration servers, where a coverage file is needed for subsequent processing, but no local report needs to be viewed. For example, tests run on GitHub Actions could produce a .coverage file for use with Coveralls. 

## Real Use
Does Coverage and reports it in a xml file in the tests dir:

`pytest --cov-report term --cov-report=xml:tests/cov.xml --cov=app tests/`

## Combining with Mutation Testing
Both Pytest-cov and Mutatest are available via Conda!

Here we use mutation testing with coverage to get a full report and make a .coverage file (.coverage files are used by the [Genome](https://mutatest.readthedocs.io/en/latest/api_tutorial/api_tutorial.html#genome-basics))

`mutatest -s . -n 5 -m sd -r 314 -t "pytest --cov=app tests/"`

```
-s = source of code to mutate
-n = number of locations in code to mutate
-m = mode
-t = test commands
```