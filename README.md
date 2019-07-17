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
* tqdm - Optionnal: progression bar
* Graph-tool - Optionnal: only one function requires it


```shell
$ pip install numpy
$ pip install panda
$ pip install matplotlib 
$ pip install tqdm 
```

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
* topic 
* category

### YAML file

Codes that use LogDiv are directed by a YAML file: if you want to modify entry files, or the features you want to compute, 
you just need to modify the YAML file, not the code itself.
This file is self-explanatory.

## Examples

You dispose of two examples to familiarize yourself with LogDiv:
* Example 1 uses a short dataset to show how to use LogDiv
* Example 2 uses a dataset of more than 500 thousands of requests to show what kind of results can be obtained

These examples (dataset, script and yaml file) can be found in *datasets* directory.

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

### Example 2

![](example_2.png)

