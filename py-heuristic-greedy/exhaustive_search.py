#!/usr/bin/env python3

import argparse
import itertools

import tqdm

from constants import min_swaps
from util import all_friend_pairs, new_friend_pairs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Check every possible sequence of swaps for a table of the specified size, 
        counting the number of results that match the minimum number of swaps required
        and displays one such sequence of swaps at the end.
        """,
    )
    parser.add_argument("table_size", type=int, help="Number of people at the table.")
    args = parser.parse_args()

    table_size = args.table_size
    # we start with a known upper bound on the number of swaps required.
    current_min_swap_count = min_swaps.get(
        table_size, table_size * (table_size - 1) // 2
    )
    all_possible_swaps = itertools.combinations(range(table_size), 2)

    initial_seating_arrangement = list(range(table_size))
    initial_friend_pairs = all_friend_pairs(initial_seating_arrangement)

    pbar = tqdm.tqdm(
        itertools.product(all_possible_swaps, repeat=current_min_swap_count)
    )

    min_swap_count = current_min_swap_count
    covering_swaps = None
    num_distinct_solutions = 0

    for candidate_swaps in pbar:
        pbar.set_description(
            "min swaps: {}, distinct solns: {}".format(
                min_swap_count, num_distinct_solutions
            )
        )
        seating_arrangement = initial_seating_arrangement[::]
        existing_friend_pairs = initial_friend_pairs.copy()
        num_total_friend_pairs = table_size * (table_size - 1) / 2

        for (t, swap) in enumerate(candidate_swaps):
            (i, j) = swap
            nfp = new_friend_pairs(seating_arrangement, existing_friend_pairs, swap)
            p_i = seating_arrangement[i]
            p_j = seating_arrangement[j]
            seating_arrangement[j] = p_i
            seating_arrangement[i] = p_j
            existing_friend_pairs = existing_friend_pairs.union(nfp)
            if len(existing_friend_pairs) == num_total_friend_pairs:
                if t + 1 < min_swap_count or covering_swaps is None:
                    min_swap_count = t + 1
                    covering_swaps = candidate_swaps[: t + 1]
                    num_distinct_solutions = 0
                else:
                    num_distinct_solutions += 1
                pbar.set_description(
                    "min swaps: {}, distinct solns: {}".format(
                        min_swap_count, num_distinct_solutions
                    )
                )
                break

    pbar.close()

    print("Covering swaps: {}".format(covering_swaps))
