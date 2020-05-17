#!/usr/bin/env python3

import argparse
import os
import pickle

from swapper import nameToSwapper
from swapper_util import SwapperRunner, get_checkpoint_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Conduct a heuristic search for the minimum number of swaps required for
        a table of the specified size. For each trial, the `swapper` specified
        is used to generate the next swap that we will attempt. Data is saved to 
        a checkpoint every 60 seconds, if a trial matching or improving on the
        high score is found, and at the end of all trials. The search resumes 
        from an existing checkpoint if available.
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("table_size", type=int, help="Number of people at the table.")
    parser.add_argument(
        "--swapper",
        type=lambda x: nameToSwapper[x],
        help="Swapper that selects the next swap to attempt.",
        default="GreedySwapper",
        choices=list(nameToSwapper.keys()),
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="""If specified, print information in corresponding checkpoint file
        and exit.
        """,
    )
    parser.add_argument(
        "--num-trials", type=int, help="Number of trials to run.", default=10000,
    )
    args = parser.parse_args()

    if args.info:
        cp_file = get_checkpoint_file(args.swapper, args.table_size)
        if os.path.isfile(cp_file):
            with open(cp_file, "rb") as f:
                # some legacy pickle files have 3 fields; the third is extraneous
                [i, best_swap_sequences] = pickle.load(f)[:2]
            print(
                "\nCollecting log information when running {} on a table of size {}.".format(
                    args.swapper, args.table_size
                )
            )
            print(
                "Trials at checkpoint: {}, high score: {}.".format(
                    i, len(best_swap_sequences[0][1])
                )
            )
            print("Trials achieving high score: {}.".format(len(best_swap_sequences)))
            if len(best_swap_sequences) > 0:
                print("Sample swap sequence: {}".format(best_swap_sequences[0][1]))
        else:
            print("No checkpoint file found.")
    else:
        SwapperRunner(args.swapper, args.table_size).run(args.num_trials)
