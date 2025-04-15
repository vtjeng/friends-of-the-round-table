#include <iostream>
#include <vector>
#include <set>
#include <unordered_set>
#include <algorithm>
#include <random>
#include <chrono>
#include <tuple>
#include <cstring>

using namespace std;

// Hash function for pair<int, int>
struct pair_hash {
    size_t operator()(const pair<int, int>& p) const {
        return hash<int>()(p.first) ^ (hash<int>()(p.second) << 1);
    }
};

// Helper function: returns all friend pairs in a seating arrangement (circular table)
unordered_set<pair<int, int>, pair_hash> all_friend_pairs(const vector<int>& seating) {
    unordered_set<pair<int, int>, pair_hash> friends;
    int n = seating.size();
    friends.reserve(n);
    for (int i = 0; i < n; ++i) {
        auto [a, b] = minmax(seating[i], seating[(i + 1) % n]);
        friends.insert({a, b});
    }
    return friends;
}

// Helper: sorted pair for positions i and j
pair<int, int> get_pair(const vector<int>& seating, int i, int j) {
    int n = seating.size();
    auto [a, b] = minmax(seating[(i + n) % n], seating[(j + n) % n]);
    return {a, b};
}

// Returns new friend pairs generated by swap (i, j)
vector<pair<int, int>> new_friend_pairs(const vector<int>& seating, const unordered_set<pair<int, int>, pair_hash>& existing, pair<int, int> swap) {
    int i = swap.first, j = swap.second;
    vector<pair<int, int>> candidates = {
        get_pair(seating, i, j - 1),
        get_pair(seating, i, j + 1),
        get_pair(seating, j, i - 1),
        get_pair(seating, j, i + 1)
    };
    vector<pair<int, int>> result;
    for (auto& p : candidates) {
        if (p.first != p.second && existing.count(p) == 0) {
            result.push_back(p);
        }
    }
    return result;
}

int num_new_friend_pairs(const vector<int>& seating, const unordered_set<pair<int, int>, pair_hash>& existing, pair<int, int> swap) {
    return new_friend_pairs(seating, existing, swap).size();
}

#include <unordered_set>

struct GreedySwapper {
    vector<int> seating;
    unordered_set<pair<int, int>, pair_hash> existing;
    vector<pair<int, int>> swaps;
    int n;
    vector<pair<int, int>> all_possible_swaps;

    // For diagnostics: serialize all_possible_swaps
    string swaps_order_string() const {
        string s;
        for (auto& p : all_possible_swaps) {
            s += to_string(p.first) + "," + to_string(p.second) + ";";
        }
        return s;
    }
    // Serialize the sequence of swaps performed
    string swap_sequence_string() const {
        string s;
        for (auto& p : swaps) {
            s += to_string(p.first) + "," + to_string(p.second) + ";";
        }
        return s;
    }

    GreedySwapper(int table_size) : seating(table_size) {
        n = table_size;
        for (int i = 0; i < n; ++i) seating[i] = i;
        existing = all_friend_pairs(seating);
        // Generate all possible swaps
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                all_possible_swaps.emplace_back(i, j);
            }
        }
    }

    pair<int, int> generate_swap() {
        vector<pair<int, int>> max_swaps;
        int max_new_friends = 1;
        for (auto& swap : all_possible_swaps) {
            int num_new = num_new_friend_pairs(seating, existing, swap);
            if (num_new == max_new_friends) {
                max_swaps.push_back(swap);
            } else if (num_new > max_new_friends) {
                max_new_friends = num_new;
                max_swaps = {swap};
                if (num_new == 4) break;
            }
        }
        return max_swaps[0];
    }

    void do_swap(pair<int, int> swap) {
        int i = swap.first, j = swap.second;
        vector<pair<int, int>> nfp = new_friend_pairs(seating, existing, swap);
        swap_values(seating[i], seating[j]);
        for (auto& p : nfp) existing.insert(p);
        swaps.push_back(swap);
    }

    bool is_everyone_friends() const {
        return existing.size() == static_cast<size_t>((n * (n - 1)) / 2);
    }

    int num_swaps() const { return swaps.size(); }

    static void swap_values(int& a, int& b) {
        int t = a; a = b; b = t;
    }
};

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <table_size> [--num-trials N]\n";
        return 1;
    }
    int table_size = atoi(argv[1]);
    int num_trials = 10000;
    for (int i = 2; i < argc; ++i) {
        if (strcmp(argv[i], "--num-trials") == 0 && i + 1 < argc) {
            num_trials = atoi(argv[++i]);
        }
    }
    mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
    int best_swaps = table_size * (table_size - 1) / 2;
    vector<pair<int, int>> best_sequence;
    int print_interval = 1000;
    unordered_set<string> unique_swap_orders; // Track unique all_possible_swaps orderings
    unordered_set<string> unique_swap_sequences; // Track unique swap sequences
    for (int t = 0; t < num_trials; ++t) {
        GreedySwapper swapper(table_size);
        // Shuffle all_possible_swaps with global rng
        shuffle(swapper.all_possible_swaps.begin(), swapper.all_possible_swaps.end(), rng);
        while (!swapper.is_everyone_friends() && swapper.num_swaps() < best_swaps) {
            auto s = swapper.generate_swap();
            swapper.do_swap(s);
        }
        // Track the swap order for this trial
        unique_swap_orders.insert(swapper.swaps_order_string());
        // Track the swap sequence for this trial
        // (serialize the sequence of swaps performed)
        unique_swap_sequences.insert(swapper.swap_sequence_string());
        // Diagnostics: print unique swap sequence info for this trial
        if ((t+1) % print_interval == 0) {
            cout << "\rTrial " << (t+1) << ": " << swapper.swaps.size() << " swaps, "
                 << unique_swap_sequences.size() << " unique swap sequences tried" << flush;
        }
        if (swapper.is_everyone_friends() && swapper.num_swaps() <= best_swaps) {
            best_swaps = swapper.num_swaps();
            best_sequence = swapper.swaps;
        }
    }
    cout << endl;
    cout << "Best number of swaps: " << best_swaps << "\n";
    cout << "Swap sequence: ";
    for (auto& s : best_sequence) {
        cout << "(" << s.first << "," << s.second << ") ";
    }
    cout << endl;
    cout << "Unique all_possible_swaps orderings seen: " << unique_swap_orders.size() << endl;
    cout << "Unique swap sequences tried: " << unique_swap_sequences.size() << endl;
    return 0;
}
