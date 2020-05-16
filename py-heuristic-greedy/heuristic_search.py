#!/usr/bin/env python3

import argparse
import os
import pickle

from constants import CHECKPOINT_DIR
from swapper import nameToSwapper
from swapper_util import get_best_swap_sequence_logged

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Conduct a heuristic search for the minimum number of swaps required for
        a table of the specified size. For each trial, the `swapper` specified
        is used to generate the next swap that we will attempt.
        """
    )
    parser.add_argument("table_size", type=int, help="Number of people at the table.")
    parser.add_argument(
        "--swapper",
        type=str,
        help="Swapper that selects the next swap to attempt",
        default="GreedySwapper",
        choices=list(nameToSwapper.keys()),
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="If specified, attempts to find checkpoint file and provides information in checkpoint file if found.",
    )
    args = parser.parse_args()

    if args.info:
        cp_dir = os.path.join(CHECKPOINT_DIR, args.swapper)
        cp_file = os.path.join(cp_dir, str(args.table_size) + ".pickle")
        if os.path.isfile(cp_file):
            with open(cp_file, "rb") as f:
                [i, best_swap_sequences, current_min_swap_num] = pickle.load(f)
            print(
                "\nCollecting log information when running {} on a table of size {}.".format(
                    args.swapper, args.table_size
                )
            )
            print(
                "Trials at checkpoint: {}, high score: {}.".format(
                    i, current_min_swap_num
                )
            )
            print("Trials achieving high score: {}.".format(len(best_swap_sequences)))
            if len(best_swap_sequences) > 0:
                print("Sample swap sequence: {}".format(best_swap_sequences[0][1]))
        else:
            print("No checkpoint file found.")
    else:
        get_best_swap_sequence_logged(nameToSwapper[args.swapper], args.table_size)