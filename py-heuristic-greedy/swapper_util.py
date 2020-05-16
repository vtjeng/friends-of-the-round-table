import collections
import logging
import os
import pickle

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


def get_best_swap_sequence(swapper, num_trials, table_size, verbose=False):
    # TODO: factor out the common logic between get_best_swap_sequence and get_best_swap_sequence_logger
    """ Runs the provided swapper for a specified number of trials, returning the swap sequence that makes everyone
    friends in the minimal number of steps.

    Several attempts are made to improve efficiency - in particular, we terminate early if there is no possibility
    of improving on the current score.

    :param swapper: Class that is used to select the next swap to be executed.
    :param num_trials:
    :param table_size:
    :param verbose:
    :return: Tuple of the minimum number of swaps found, and a list of tuples (iteration_number, swap_sequence)
        achieving that minimum.
    """
    if verbose:
        print(
            "Running {swapper_name} with a table of size {table_size}".format(
                swapper_name=swapper.__name__, table_size=table_size
            )
        )
    best_swap_sequences = list()
    attempted_swap_sequences = set()

    # the minimum number of swaps is bounded above by the number of pairs of friends since a greedy algorithm can always
    # form at least one new friendship with every swap
    current_min_swap_num = min_swaps.get(table_size, table_size * (table_size - 1) / 2)
    for i in range(num_trials):
        s = swapper(list(range(table_size)))
        while not s.is_everyone_friends() and len(s.swaps) < current_min_swap_num:
            # Trying to terminate earlier here by checking the number of friend pairings outstanding
            # and bounding the number of steps to get there by dividing that number by 4 does not seem to
            # improve performance significantly as per average cProfile results.
            swap = s.generate_swap()
            s.do_swap(swap)
        attempted_swap_sequences.add(tuple(s.swaps))
        if s.is_everyone_friends():
            # You're guaranteed to have tied or beat the high-score due to the early termination condition above.
            if len(s.swaps) == current_min_swap_num:
                if verbose:
                    print("Trial #{} tied the high score.".format(i))
            else:
                current_min_swap_num = len(s.swaps)
                best_swap_sequences = []
                if verbose:
                    print(
                        "Trial #{} hit a new high score, using a total of {} swaps.".format(
                            i, current_min_swap_num
                        )
                    )
                    print(
                        "\tSwap sequence: {sample_swaps}".format(sample_swaps=s.swaps)
                    )
            best_swap_sequences.append((i, s.swaps))
        if verbose and i % (num_trials / 100) == 0:
            print("Trial #{}".format(i))
            prop_repeated_trials = 1 - len(attempted_swap_sequences) / float(i + 1)
            print(
                "\tProportion of repeated swap sequences is {}".format(
                    prop_repeated_trials
                )
            )
            print(
                "\tNumber of fresh trials is {}".format(len(attempted_swap_sequences))
            )

    if verbose:
        print("get_best_swap complete.")

    return current_min_swap_num, best_swap_sequences


def get_best_swap_sequence_logged(swapper, table_size):
    """ Runs the provided swapper for a specified number of trials, returning the swap sequence that makes everyone
    friends in the minimal number of steps.

    Several attempts are made to improve efficiency - in particular, we terminate early if there is no possibility
    of improving on the current score.

    :param swapper: Class that is used to select the next swap to be executed.
    :param table_size:
    :return: Tuple of the minimum number of swaps found, and a list of tuples (iteration_number, swap_sequence)
        achieving that minimum.
    """
    ## Start logging
    log_dir = os.path.join(LOGS_DIR, swapper.__name__)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, str(table_size) + ".log")
    FORMAT = "%(asctime)s %(levelno)s %(message)s"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format=FORMAT)
    # Simultaneously print to stderr to allow tracking of performance.
    logging.getLogger().addHandler(logging.StreamHandler())

    ## Initialize from a checkpoint if it exists
    cp_dir = os.path.join(CHECKPOINT_DIR, swapper.__name__)
    os.makedirs(cp_dir, exist_ok=True)
    cp_file = os.path.join(cp_dir, str(table_size) + ".pickle")
    if os.path.isfile(cp_file):
        with open(cp_file, "rb") as f:
            [i, best_swap_sequences, current_min_swap_num] = pickle.load(f)
        logging.debug(
            "Restarted from checkpoint at trial #{} with high score at {}.".format(
                i, current_min_swap_num
            )
        )
    else:
        i = 1
        best_swap_sequences = list()
        current_min_swap_num = min_swaps.get(
            table_size, table_size * (table_size - 1) // 2
        )
        logging.debug("Starting with target score at {}.".format(current_min_swap_num))

    while True:
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
                # TODO: Don't print out full sample swap sequence - it's way too much!!
                logging.info(
                    "\tSwap sequence: {sample_swaps}".format(sample_swaps=s.swaps)
                )
            best_swap_sequences.append((i, s.swaps))
        i += 1
        if i % 200 == 0:
            # correcting for off-by-1 issue here.
            logging.debug("Trial #{} - checkpoint saved.".format(i))
            with open(cp_file, "wb") as f:
                pickle.dump([i, best_swap_sequences, current_min_swap_num], f)


def get_best_swap_sequences(swapper, num_trials, table_sizes):
    """ Get the best swap sequences for a range of numbers of people, and print summary data.

    :param swapper:
    :param num_trials:
    :param table_sizes:
    :return:
    """
    print("Running {swapper_name}".format(swapper_name=swapper.__name__))

    for i in table_sizes:
        (min_swap_num, best_swap_sequences) = get_best_swap_sequence(
            swapper, num_trials=num_trials, table_size=i, verbose=True
        )
        (min_trials, sample_swaps) = best_swap_sequences[0]
        print(
            "Table size: {table_size}, Minimum swaps: {min_swap_num}, Trials to reach minimum: {min_trials}".format(
                table_size=i, min_swap_num=min_swap_num, min_trials=min_trials
            )
        )
        print(
            "\tTrials achieving minimum swap count: {}".format(len(best_swap_sequences))
        )
        print(
            "\tSample swap sequence: {sample_swaps}".format(sample_swaps=sample_swaps)
        )
