# C++ Heuristic Greedy Search

This directory contains a C++ implementation of the heuristic greedy search for the minimum number of swaps required for a table of a specified size. The algorithm is adapted from the Python version in `py-heuristic-greedy`.

## Usage

Build the project with:

```
make
```

Run the program with:

```
./heuristic_search <table_size> [--num-trials N]
```

- `<table_size>`: Number of people at the table (required).
- `--num-trials N`: Number of trials to run (default: 10000).

## Description

Each trial attempts to find a minimal swap sequence such that everyone becomes friends with everyone else, using a greedy heuristic to maximize new friendships per swap.

## Files

- `heuristic_search.cpp`: Main implementation.
- `Makefile`: For building the project.

## Benchmarking Results

The following benchmarks were run with 10,000 trials for various table sizes, run on a Windows 10 machine with WSL and an Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz.

| Table Size | Time (seconds) | Best Swaps Found |
| ---------- | -------------- | ---------------- |
| 10         | <1             | 10               |
| 15         | 2.64           | 26               |
| 20         | 9.57           | 49               |
| 25         | 25.18          | 79               |
| 30         | 55.91          | 116              |
| 35         | 111            | 161              |
| 40         | 187            | 211              |
