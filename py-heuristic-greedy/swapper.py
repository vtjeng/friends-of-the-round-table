import abc
import itertools
import random

import numpy as np

from util import all_friend_pairs, new_friend_pairs, num_new_friend_pairs


class AbstractSwapper(object):
    def __init__(self, initial_seating_arrangement):
        # mutates during operation
        self.seating_arrangement = initial_seating_arrangement
        self.existing_friend_pairs = all_friend_pairs(self.seating_arrangement)
        self.swaps = []

        # stays fixed
        self.n = len(self.seating_arrangement)
        self.num_total_friend_pairs = self.n * (self.n - 1) / 2
        self.all_possible_swaps = list(itertools.combinations(range(self.n), 2))
        # Randomly shuffle the list of possible swaps.
        np.random.shuffle(self.all_possible_swaps)

    @abc.abstractmethod
    def generate_swap(self):
        return

    def do_swap_v1(self, swap):
        # slow (but known to be correct) way of updating existing friend pairs
        (i, j) = swap
        p_i = self.seating_arrangement[i]
        p_j = self.seating_arrangement[j]
        self.seating_arrangement[j] = p_i
        self.seating_arrangement[i] = p_j
        self.existing_friend_pairs = self.existing_friend_pairs.union(
            all_friend_pairs(self.seating_arrangement)
        )
        self.swaps.append(swap)

    def do_swap(self, swap):
        # faster way of updating friend pairs that we currently use.
        (i, j) = swap
        nfp = new_friend_pairs(
            self.seating_arrangement, self.existing_friend_pairs, swap
        )
        p_i = self.seating_arrangement[i]
        p_j = self.seating_arrangement[j]
        self.seating_arrangement[j] = p_i
        self.seating_arrangement[i] = p_j
        self.existing_friend_pairs = self.existing_friend_pairs.union(nfp)
        self.swaps.append(swap)

    def is_everyone_friends(self):
        """

        :return: True if everyone on the table has been introduced to everyone else, and False otherwise
        """
        return len(self.existing_friend_pairs) == self.num_total_friend_pairs

    def num_remaining_friend_pairs(self):
        return self.num_total_friend_pairs - len(self.existing_friend_pairs)


class RandomSwapper(AbstractSwapper):
    def generate_swap(self):
        return random.choice(self.all_possible_swaps)


class GreedySwapper(AbstractSwapper):
    def generate_swap(self):
        max_swaps = []
        max_new_friends = 1
        for swap in self.all_possible_swaps:
            num_new_friends = num_new_friend_pairs(
                self.seating_arrangement, self.existing_friend_pairs, swap
            )
            if num_new_friends == max_new_friends:
                max_swaps.append(swap)
            elif num_new_friends > max_new_friends:
                max_new_friends = num_new_friends
                max_swaps = [swap]
                if num_new_friends == 4:
                    # Safe to terminate here since self.all_possible_swaps is randomly sorted.
                    break

        return random.choice(max_swaps)


class SubsetGreedySwapper(AbstractSwapper):
    """
    Checks only a subset of the possible swaps.
    """

    def generate_swap(self):
        max_swaps = []
        max_new_friends = 1
        # TODO: do not hardcode the fraction we're checking.
        i = 0

        while i < len(self.all_possible_swaps) or len(max_swaps) == 0:
            swap = self.all_possible_swaps[i]
            num_new_friends = num_new_friend_pairs(
                self.seating_arrangement, self.existing_friend_pairs, swap
            )
            if num_new_friends == max_new_friends:
                max_swaps.append(swap)
            elif num_new_friends > max_new_friends:
                max_new_friends = num_new_friends
                max_swaps = [swap]
                if max_new_friends == 4:
                    # we've hit the max number of new friends
                    break
            i += 1

        return random.choice(max_swaps)


class ImpatientGreedySwapper(AbstractSwapper):
    """
    Tries to make a lot of friends initially, but slowly just gives up.

    More specifically, we have a threshold that starts at 4 but backs off to the expected mean.
    """

    def __init__(self, initial_seating_arrangement):
        super(ImpatientGreedySwapper, self).__init__(initial_seating_arrangement)
        # This is exactly the number of expected new friends that can be made, by linearity of expectation!
        self.expected_new_friends = 4 * (
            self.num_remaining_friend_pairs() / self.num_total_friend_pairs
        )

    def generate_swap(self):
        max_swaps = []
        max_new_friends = 1
        i = 0

        for (i, swap) in enumerate(self.all_possible_swaps):
            swap = self.all_possible_swaps[i]
            num_new_friends = num_new_friend_pairs(
                self.seating_arrangement, self.existing_friend_pairs, swap
            )
            if num_new_friends == max_new_friends:
                max_swaps.append(swap)
            elif num_new_friends > max_new_friends:
                max_new_friends = num_new_friends
                max_swaps = [swap]
            target_new_friends = 4 - (4 - self.expected_new_friends) * (
                i / float(len(self.all_possible_swaps) - 1)
            )
            if max_new_friends >= target_new_friends and len(max_swaps) > 0:
                # we've hit our target and found an example - time to quit.
                break

        return random.choice(max_swaps)


class WeightedSwapper(AbstractSwapper):
    def generate_swap(self):
        # if we maintain and update d at each step, we have the potential to be much quicker

        d = {
            swap: num_new_friend_pairs(
                self.seating_arrangement, self.existing_friend_pairs, swap
            )
            for swap in self.all_possible_swaps
        }
        swap = d.keys()
        p_swap_raw = map(lambda x: np.exp(3 * x), d.itervalues())
        p_swap = p_swap_raw / sum(p_swap_raw)

        # all I want to do is have a weighted choice of tuples. is that too hard?
        return swap[np.random.choice(range(len(swap)), p=p_swap)]


nameToSwapper = {
    "GreedySwapper": GreedySwapper,
    "ImpatientGreedySwapper": ImpatientGreedySwapper,
    "SubsetGreedySwapper": SubsetGreedySwapper,
    "WeightedSwapper": WeightedSwapper,
}
