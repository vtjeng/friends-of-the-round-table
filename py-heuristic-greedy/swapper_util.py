import collections
import logging
import os
import pickle
import tqdm
import time

from constants import min_swaps, LOGS_DIR, CHECKPOINT_DIR


def profile_swapper(swapper, num_trials, table_size, show_plot=False):

    """ Tests the performance of a swapper, looking at the distribution of the number of swops required for each of
    the trials.

    :param swapper: Class that is used to select the next swap to be executed.
    :param num_trials:
    :param table_size:
    :param show_plot: True if you want to view a plot of the distribution of number of swops.
    :return: Counter of number of swops required for each trial.
    """

    c = collections.Counter()
    for i in range(num_trials):
        s = swapper(range(table_size))
        while not s.is_everyone_friends():
            s.do_swap(s.generate_swap())
        num_swaps = len(s.swaps)
        c[num_swaps] += 1

    # TODO: Temporarily disabling option to show plot as importing matplotlib takes time (and I can't seem to get it working well anyway)
    # if show_plot:
    #     matplotlib.pyplot.scatter(c.keys(), c.values())
    #     matplotlib.pyplot.show()

    return c


def get_best_swap_sequence_logged(swapper, table_size, num_trials, checkpoint_interval_seconds=60):
    """ Runs the provided swapper for a specified number of trials, returning the swap sequence that makes everyone
    friends in the minimal number of steps.

    Several attempts are made to improve efficiency - in particular, we terminate early if there is no possibility
    of improving on the current score.

    Saves results to a checkpoint every 200 trials or if a new high score is reached.

    :param swapper: Class that is used to select the next swap to be executed.
    :type swapper: AbstractSwapper
    :param table_size:
    :type table_size: int
    :param num_trials:
    :type num_trials: int
    :param checkpoint_interval_seconds: number of seconds between checkpoints
    :type checkpoint_interval_seconds: float
    :return: Tuple of the minimum number of swaps found, and a list of tuples (iteration_number, swap_sequence)
        achieving that minimum.
    """
    ## Start logging
    log_file = get_log_file(swapper, table_size)
    FORMAT = "%(asctime)s %(levelno)s %(message)s"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format=FORMAT)

    ## Initialize from a checkpoint if it exists
    cp_file = get_checkpoint_file(swapper, table_size)
    if os.path.isfile(cp_file):
        with open(cp_file, "rb") as f:
            [i, best_swap_sequences, current_min_swap_num] = pickle.load(f)
        logging.debug(
            "Restarted from checkpoint at trial #{} with high score at {}.".format(
                i, current_min_swap_num
            )
        )
    else:
        i = 0
        best_swap_sequences = list()
        current_min_swap_num = min_swaps.get(
            table_size, table_size * (table_size - 1) // 2
        )
        logging.debug("Starting with target score at {}.".format(current_min_swap_num))

    last_checkpoint = i
    last_checkpoint_time = time.time()
    with tqdm.trange(num_trials) as pbar:
        for _ in pbar:
            pbar.set_description(
                "trial: {}, last checkpoint: {}. min swaps: {}.".format(
                    i, last_checkpoint, current_min_swap_num
                )
            )
            i += 1
            s = swapper(list(range(table_size)))
            while not s.is_everyone_friends() and len(s.swaps) < current_min_swap_num:
                # Trying to terminate earlier here by checking the number of friend pairings outstanding
                # and bounding the number of steps to get there by dividing that number by 4 does not seem to
                # improve performance significantly as per average cProfile results.
                swap = s.generate_swap()
                s.do_swap(swap)
            if s.is_everyone_friends():
                # You're guaranteed to have tied or beat the high-score due to the early termination condition above.
                if len(s.swaps) == current_min_swap_num:
                    logging.debug(
                        "Trial #{} tied the high score, at {}.".format(
                            i, current_min_swap_num
                        )
                    )
                else:
                    current_min_swap_num = len(s.swaps)
                    best_swap_sequences = []
                    logging.info(
                        "Trial #{} hit a new high score at {}.".format(
                            i, current_min_swap_num
                        )
                    )
                    with open(cp_file, "wb") as f:
                        last_checkpoint = i
                        pickle.dump([i, best_swap_sequences, current_min_swap_num], f)
                best_swap_sequences.append((i, s.swaps))
            if time.time() - last_checkpoint_time > checkpoint_interval_seconds:
                last_checkpoint_time = time.time()
                logging.debug("Trial #{} - checkpoint saved.".format(i))
                with open(cp_file, "wb") as f:
                    last_checkpoint = i
                    pickle.dump([i, best_swap_sequences, current_min_swap_num], f)


def get_checkpoint_file(swapper, table_size):
    return os.path.join(get_checkpoint_dir(swapper), str(table_size) + ".pickle")


def get_checkpoint_dir(swapper):
    cp_dir = os.path.join(CHECKPOINT_DIR, swapper.__name__)
    os.makedirs(cp_dir, exist_ok=True)
    return cp_dir


def get_log_file(swapper, table_size):
    return os.path.join(get_log_directory(swapper), str(table_size) + ".log")


def get_log_directory(swapper):
    log_dir = os.path.join(LOGS_DIR, swapper.__name__)
    os.makedirs(log_dir, exist_ok=True)
    return log_dir
