#!/usr/bin/env python3

from constants import PWD, CHECKPOINT_DIR
import os
import pickle

for (dirpath, dirnames, filenames) in os.walk(CHECKPOINT_DIR):
    print(os.path.split(dirpath)[-1])
    for filename in sorted(filenames, key=lambda x: int(os.path.splitext(x)[0])):
        cp_file = os.path.join(dirpath, filename)
        with open(cp_file, "rb") as f:
            [i, best_swap_sequences] = pickle.load(f)[:2]
        print(
            "\t{table_size} - best: {high_score:>4}, seen in {num_achieved:>4}/{num_trials:>11}".format(
                table_size=os.path.splitext(filename)[0],
                num_trials=i,
                high_score=len(best_swap_sequences[0][1]),
                num_achieved=len(best_swap_sequences),
            )
        )
