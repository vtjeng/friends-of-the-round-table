A heuristic approach implemented in Python. Your entry point is the script `heuristic_search.py`

```
$ ./heuristic_search.py --help
usage: heuristic_search.py [-h]
                           [--swapper {GreedySwapper,ImpatientGreedySwapper,SubsetGreedySwapper,WeightedSwapper}]
                           [--info] [--num-trials NUM_TRIALS]
                           table_size

Conduct a heuristic search for the minimum number of swaps required for a
table of the specified size. For each trial, the `swapper` specified is used
to generate the next swap that we will attempt. Data is saved to a checkpoint
every 60 seconds or if a trial matching or improving on the high score is
found; the search resumes from an existing checkpoint if available.

positional arguments:
  table_size            Number of people at the table.

optional arguments:
  -h, --help            show this help message and exit
  --swapper {GreedySwapper,ImpatientGreedySwapper,SubsetGreedySwapper,WeightedSwapper}
                        Swapper that selects the next swap to attempt.
                        (default: GreedySwapper)
  --info                If specified, print information in corresponding
                        checkpoint file and exit. (default: False)
  --num-trials NUM_TRIALS
                        Number of trials to run. (default: 10000)
```

`exhaustive_search.py` is provided for a sanity check (but is very slow).

```
$ ./exhaustive_search.py --help
usage: exhaustive_search.py [-h] table_size

Check every possible sequence of swaps for a table of the specified size,
counting the number of results that match the minimum number of swaps required
and displays one such sequence of swaps at the end.

positional arguments:
  table_size  Number of people at the table.

optional arguments:
  -h, --help  show this help message and exit
```

If you'd like to see all of the checkpoint information at once, you can use `summarize_heuristic_search_checkpoint_info.py`.

```
$ ./summarize_heuristic_search_checkpoint_info.py
checkpoint
GreedySwapper
        5 - best:    3, seen in 2630/       2630
        7 - best:    4, seen in  259/        500
        8 - best:    7, seen in  398/        500
        9 - best:    8, seen in    9/        477
        10 - best:   10, seen in   83/       9637
        11 - best:   12, seen in    6/      10000
        13 - best:   17, seen in   13/   71260800
        14 - best:   20, seen in    1/   52056000
        15 - best:   24, seen in  242/ 1054258373
        16 - best:   28, seen in   21/  114931400
        17 - best:   32, seen in   20/  651667000
        18 - best:   37, seen in   30/   70074800
        19 - best:   41, seen in    1/  363457000
        20 - best:   46, seen in    1/  135992600
        21 - best:   52, seen in    9/  151577400
        22 - best:   57, seen in    1/  124422200
        23 - best:   64, seen in   25/  104285000
        24 - best:   70, seen in    5/   68220000
        25 - best:   77, seen in   14/   26664400
        26 - best:   84, seen in   15/   23223200
        27 - best:   91, seen in   13/   19822400
        29 - best:  108, seen in    1/      38000
        30 - best:  114, seen in    3/    4778200
        40 - best:  210, seen in    4/     914800
        45 - best:  267, seen in    1/    1312800
        50 - best:  334, seen in    1/      48600
        55 - best:  405, seen in    2/     438198

```

## Benchmarking Results

The following benchmarks were run with 10,000 trials for various table sizes, run on a Windows 10 machine with WSL and an Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz.

| Table Size | Time (seconds) | Best Swaps Found |
| ---------- | -------------- | ---------------- |
| 10         | 6.26           | 10               |
| 15         | 25.78          | 26               |
| 20         | 76             | 49               |
| 25         | 177            | 79               |
| 30         | 370            | 116              |
