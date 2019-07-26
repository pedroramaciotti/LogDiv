# LogDiv: A Python Module for Computing Diversity in Transaction Logs

LogDiv is a Python module for the computation of the diversity of items requested by users in transaction logs.

It takes two inputs:

1) A log file with transactions.
2) A file with item atributes.

Computing the diversity of items requested by users is a task of interest in many fields, such as sociology, recommender systems, e-commerce, and media studies. Check the example below.

## Getting Started

### Prerequisites

LogDiv requires:

* Python
* Numpy - Essential
* Pandas - Essential
* Matplotlib - Essential
* pyyaml - Essential
* scikit-learn - Essential
* tqdm - Optional: progression bar, only one function requires it
* Graph-tool - Optional: only one function requires it


```shell
$ python3 -m pip install numpy
$ python3 -m pip install panda
$ python3 -m pip install matplotlib 
$ python3 -m pip install pyyaml
$ python3 -m pip install scikit-learn
$ python3 -m pip install tqdm 
```

Installing Graph-tool is more complicated: https://git.skewed.de/count0/graph-tool/wikis/installation-instructions

### Installing

To install LogDiv, you need to execute:

```shell
$ pip install logdiv
```

## Specification

### Entries format

LogDiv needs a specific format of entries to run:

- A file describing all requests under a table format, whose fields are:
* user ID
* timestamp
* requested item ID
* referrer item ID

- A file describing all pages visited under a table format, whose fields are:
* item ID
* classification 1 
* classification 2
* ...

### YAML file

Codes that use LogDiv are directed by a YAML file: if you want to modify entry files, or the features you want to compute, 
you just need to modify the YAML file, not the code itself.

YAML file are similar to JSON file, once you load them, they take the form of a dictionnary. In your codes, you have for instance 
a function that take a parameter that need to be changed often. You can give to your function the key of the dictionnary, and then 
change the value in the YAML file. This allows to make less mistakes and take less time when you want to change parameters in your code.

### Documentation

If you want precision on a function of LogDiv: 
* what is the purpose of the function
* what these functions take in entry
* what they return

you need to run in a Console Python:
```python
>>> help(function)
```

## Examples

You dispose of two examples to familiarize yourself with LogDiv:
* Example 1 uses a short dataset to show how to use LogDiv
* Example 2 uses a dataset of more than 100 thousands of requests to show what kind of results can be obtained

These examples (dataset, script and yaml file) can be found in *datasets* directory. These YAML files are self-explanatory.

### Example 1
The following example illustrates the entries format of the package.

![](example.png)

|user |timestamp          |requested_item| referrer_item|
|-----|-------------------|--------------|-------------|
|user1|2019-07-03 00:00:00|v1            |v4           |
|user1|2019-07-03 00:01:00|v4            |v2           |
|user1|2019-07-03 00:01:10|v4            |v6           |
|user1|2019-07-03 00:01:20|v4            |v6           |
|user1|2019-07-03 00:02:00|v6            |v9           |
|user1|2019-07-03 03:00:00|v8            |v10          |
|user1|2019-07-03 03:01:00|v8            |v5           |
|user2|2019-07-05 12:00:00|v3            |v5           |
|user2|2019-07-05 12:00:30|v5            |v7           |
|user2|2019-07-05 12:00:45|v7            |v9           |
|user2|2019-07-05 12:01:00|v9            |v6           |
|user3|2019-07-05 18:00:00|v10           |v5           |
|user3|2019-07-05 18:01:15|v10           |v7           |
|user3|2019-07-05 18:03:35|v10           |v9           |
|user3|2019-07-05 18:06:00|v7            |v4           |
|user3|2019-07-05 18:07:22|v5            |v2           |

|item|class1  |class2  |class3 |
|----|--------|--------|-------|
|v1  |x       |\alpha  |h      |
|v2  |y       |\beta   |h      |
|v3  |y       |\beta   |f      |
|v4  |x       |\beta   |h      |
|v5  |z       |\gammma |f      |
|v6  |y       |\alpha  |h      |
|v7  |z       |\alpha  |f      |
|v8  |x       |\gammma |f      |
|v9  |y       |\alpha  |f      |
|v10 |z       |\gammma |h      |

If you want to run example 1, you need to be in the directory datasets/example1, and run:
```shell
$ python3 example_1.py
```

### Example 2

![](example_2.png)

This figure is the Gephi graph of dataset 2, where each color correspond to a different media.

The file describing requests has the same structure than the one in example 1.

The file describing pages is more concrete than the one in example 1:

|item   |media   |continent    |
|-------|--------|-------------|
|item0  |Politics|Europe       |
|item1  |Health  |Asia         |
|item2  |Politics|North America|

If you want to run example 2, you need to be in the directory datasets/example2, and run:
```shell
$ python3 example_2.py
```





