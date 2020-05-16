#!/usr/bin/env python3

from constants import PWD, CHECKPOINT_DIR
import os
import pickle

for (dirpath, dirnames, filenames) in os.walk(CHECKPOINT_DIR):
    print(os.path.split(dirpath)[-1])
    for filename in sorted(filenames):
        # print(filename)
        cp_file = os.path.join(dirpath, filename)
        with open(cp_file, "rb") as f:
            [i, best_swap_sequences, current_min_swap_num] = pickle.load(f)
        print(
            "\t{table_size} - best: {high_score:>4}, seen in {num_achieved:>4}/{num_trials:>11}".format(
                table_size=os.path.splitext(filename)[0],
                num_trials=i,
                high_score=current_min_swap_num,
                num_achieved=len(best_swap_sequences),
            )
        )
