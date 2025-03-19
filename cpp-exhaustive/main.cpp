#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <numeric>
#include <optional>
#include <string>

#include <vector>

struct SeatPair {
  // Represents an unordered pair of distinct non-negative indexes.
  int first;
  int second;
};

/**
 Converts an unordered pair of distinct non-negative indexes to a
 single non-negative index.

 (0, 1) -> 0
 (0, 2) -> 1
 (1, 2) -> 2
 (0, 3) -> 3
 ...

 Allows for information about the unordered pair of indexes {x1, x2} to be
 stored in a single array indexed by pair_to_index({x1, x2}).

 This function is a bijection, and satisfies the property that the output
 indexes will be produced "in running order":
 {pair_to_index({x1, x2}) | 0≤x1≤n ∧ 0≤x2≤n ∧ x1≠x2} = {0, 1, ..., T_{n+1}-1},
 where `T_n` is the nth triangular number.
 */
int pair_to_index(const SeatPair &input) {
  if (input.first > input.second) {
    return input.first * (input.first - 1) / 2 + input.second;
  }
  return input.second * (input.second - 1) / 2 + input.first;
}

void print(std::vector<int> const &input) {
  for (const auto &i : input) {
    std::cout << i << ", ";
  }
  std::cout << std::endl;
}

void print(std::vector<SeatPair> const &input) {
  for (const auto &i : input) {
    std::cout << "(" << i.first << ", " << i.second << "), ";
  }
  std::cout << std::endl;
}

/**
 Given a table of size `n`, determines whether it is possible for every guest
 to have sat next to every other guest at some point, given that there are
 `num_remaining_switches` available, the current configuration of guests in
 seats is `current_table`, and `adjacency_count` stores information on how many
 times guests have already sat next to each other.

 @param num_remaining_switches How many remaining switches available.
 @param current_switches List containing the pairs of seats switched such that
     `table` reaches its current state.
 @param current_table current_table[i] is the label of the guest sitting
     in the ith seat. Note that the table is "circular" (i.e. the first and
     last entries of current_table are considered to be sitting next to each
     other). guest labels are expected to be distinct and running from [0, 1,
     ..., current_table.size()-1].
 @param adjacency_count for two guests x1, x2, where x1 < x2,
     adjacency_count[pair_to_index({x1, x2})] stores the number of times x1 and
     x2 have "newly" sat next to each other. Concretely, this is initialized at
     1 for every pair of guests sitting next to each other in the initial table
     and initialized at 0 otherwise. The count is then incremented only when a
     guest moves (add 1 to the adjacency count of that guest and their new left
     and right neighbor).

 @returns A sequence of the positions of the pairs of seats being switched, or
     std::nullopt if no such sequence of length up to `num_remaining_switches`
     exists.
 */
std::optional<std::vector<SeatPair>> get_switches_recursive_helper(
    const int num_remaining_switches, std::vector<SeatPair> &current_switches,
    std::vector<int> &current_table, std::vector<int> &adjacency_count) {
  const int n = current_table.size();

  for (int i = 0; i < n - 1; ++i) {
    for (int j = i + 1; j < n; ++j) {
      // Iterate over every possible pair of seats (i, j)
      current_switches.push_back(SeatPair({i, j}));
      std::iter_swap(current_table.begin() + i, current_table.begin() + j);
      // We identify the guests that moved and take note of the
      // guests that they are sitting to the left and right of.
      // (Note that, despite the name of the variable, these guests
      // may have actually been previously sitting next to each other ---
      // consider swapping any two guests on a three-person table).
      // Array Initialization:
      // https://stackoverflow.com/questions/12844475/why-cant-simple-initialize-with-braces-2d-stdarray
      std::array<SeatPair, 4> newly_adjacent_guest_pairs = {{
          {current_table[i], current_table[(i + 1) % n]},
          {current_table[i], current_table[(i - 1 + n) % n]},
          {current_table[j], current_table[(j + 1) % n]},
          {current_table[j], current_table[(j - 1 + n) % n]},
      }};
      for (const auto &guest_pair : newly_adjacent_guest_pairs) {
        const int idx = pair_to_index(guest_pair);
        ++adjacency_count[idx];
      }

      // check if the adjacency count is positive for all pairs of guests
      if (std::all_of(adjacency_count.begin(), adjacency_count.end(),
                      [](int i) { return i > 0; })) {
        // if so, current_switches contains a "good" sequence of
        // switches (i.e., a sequence such that everyone gets to sit
        // next to everyone else)
        return current_switches;
      }

      // if not, we check if the switch we executed was the last available.
      if (num_remaining_switches > 1) {
        const std::optional<std::vector<SeatPair>> r =
            get_switches_recursive_helper(num_remaining_switches - 1,
                                          current_switches, current_table,
                                          adjacency_count);
        if (r.has_value()) {
          // if we find a good sequence of switches with the recursive
          // call, we return it
          return r;
        }
      }

      // If we get here, no sequence of switches starting with
      // `current_switches` is good. We retrace our steps, undoing the changes
      // to `adjacency_count`, `current_table`, and remove the switch from
      // `current_switches`.
      for (const auto &guest_pair : newly_adjacent_guest_pairs) {
        const int idx = pair_to_index(guest_pair);
        --adjacency_count[idx];
      }
      std::iter_swap(current_table.begin() + i, current_table.begin() + j);
      current_switches.pop_back();
    }
  }
  return {};
}

/**
 Given a table of size `n`, determines whether it is possible for every guest
 to have sat next to every other guest at some point, with up to `num_switches`
 pairs of guests switching seats.

 See
 https://math.stackexchange.com/questions/833541/making-friends-around-a-circular-table
 for full details.

 @returns A sequence of the positions of the pairs of seats being switched, or
     std::nullopt if no such sequence of length up to `num_switches` exists.
 */
std::optional<std::vector<SeatPair>> get_switches_recursive(int n,
                                                            int num_switches) {
  std::vector<SeatPair> switches;
  switches.reserve(num_switches);

  // initialize table with guest i in seat i.
  // (the specific identity of which guest gets to sit where is not
  // critical; it just matters that the labels are distinct)
  std::vector<int> table(n);
  std::iota(table.begin(), table.end(), 0);

  const int num_pairs = n * (n - 1) / 2;
  // adjacency_count is initialized to all 0s
  std::vector<int> adjacency_count(num_pairs);
  // adjacency_count is set to 1 for every pair of guests sitting
  // next to each other in the initial table arrangement
  ++adjacency_count[pair_to_index(SeatPair{table[0], table[n - 1]})];
  for (int i = 0; i < n - 1; ++i) {
    ++adjacency_count[pair_to_index(SeatPair{table[i], table[i + 1]})];
  }

  return get_switches_recursive_helper(num_switches, switches, table,
                                       adjacency_count);
}

int main() {
  int n = 7;
  int num_switches = 4;

  std::optional<std::vector<SeatPair>> v =
      get_switches_recursive(n, num_switches);
  std::cout << "For " << n << " people with " << num_switches
            << " switches:" << std::endl;
  if (v.has_value()) {
    print(v.value());
  } else {
    std::cout << "No results" << std::endl;
  }
}
