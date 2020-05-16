#!/usr/bin/env python3

import itertools

import tqdm

from constants import min_swaps
from util import all_friend_pairs, new_friend_pairs

table_size = 7
current_min_swap_num = min_swaps.get(table_size, table_size * (table_size - 1) // 2)
all_possible_swaps = itertools.combinations(range(table_size), 2)
swap_gen = itertools.product(all_possible_swaps, repeat=current_min_swap_num)
c = 0

initial_seating_arrangement = list(range(table_size))
initial_friend_pairs = all_friend_pairs(initial_seating_arrangement)

for swaps in tqdm.tqdm(swap_gen):
    seating_arrangement = initial_seating_arrangement[::]
    existing_friend_pairs = initial_friend_pairs.copy()
    num_total_friend_pairs = table_size * (table_size - 1) / 2

    for (t, swap) in enumerate(swaps):
        (i, j) = swap
        nfp = new_friend_pairs(seating_arrangement, existing_friend_pairs, swap)
        p_i = seating_arrangement[i]
        p_j = seating_arrangement[j]
        seating_arrangement[j] = p_i
        seating_arrangement[i] = p_j
        existing_friend_pairs = existing_friend_pairs.union(nfp)
        if len(existing_friend_pairs) == num_total_friend_pairs:
            print(t + 1)
            print(swaps[: t + 1])
            c += 1
            break

print("{} matched or improved upon the high score.".format(c))
