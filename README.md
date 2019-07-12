# LogDiv: A Python Module for Computing Diversity in Transaction Logs

LogDiv is a Python module for the computation of the diversity of items requested by users in transaction logs.

It takes two inputs:

1) A log file with transactions.
2) A file with item atributes.

Computing the diversity of items requested by users is a task of interest in many fields, such as sociology, recommender systems, e-commerce, and media studies. Check the example below.

## Getting Started

### Prerequisites

DivPy requires:

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
* requested page ID
* referrer page ID

- A file describing all pages visited under a table format, whose fields are:
* page ID
* topic 
* category

### YAML file

Code that use LogDiv are directed by a YAML file: if you want to modify entry files, or the features you want to compute, 
you just need to modify the YAML file, not the code itself.
This file is self-explanatory.

## Example

### Entries example
The following example illustrates the entries format of the package.

![](example.pdf)

| user_ID |   timestamp       | requested_item_ID  | referrer_item_ID  |
| ------- |:-----------------:|:------------------:|-------------------|
| USER 1  | 2019-7-1 15:20:23 |         P2         |         P1        |
| USER 3  | 2019-7-1 15:20:27 |         P4         |         P2        |
| USER 1  | 2019-7-1 15:21:01 |         P3         |         P2        |
| USER 2  | 2019-7-1 15:23:30 |         P5         |         P3        |
| USER 2  | 2019-7-1 15:23:45 |         P1         |         P5        |

| item_ID |   topic   | category  |
| ------- |:---------:|:----------|
|    v1   |  Football |  beginner |
|    v2   |  Tennis   |  pro      |
|    v3   |  Football |  beginner |
|    v4   |  Tennis   |  advanced |
|    v5   |  Rugby    |  medium   |
|    v6   |  Football |  beginner |
|    v7   |  Tennis   |  pro      |
|    v8   |  Football |  beginner |
|    v9   |  Tennis   |  advanced |
|    v10  |  Rugby    |  medium   |

In that example, the topic is a sport and the category is the level of the sport. 

### Test of LogDiv

To check if the module is successfully installed, and see what kind of results can be obtained, you can run the script in section example, using the entries given in the same directory.

