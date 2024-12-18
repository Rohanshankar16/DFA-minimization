from collections import defaultdict

def minimize_dfa(states, alphabet, transitions, start_state, final_states):
    # Step 1: Initialize the distinguishability table
    state_pairs = {(min(s1, s2), max(s1, s2)) for s1 in states for s2 in states if s1 != s2}
    distinguishable = {pair: False for pair in state_pairs}
    
    # Step 2: Mark pairs involving final and non-final states as distinguishable
    for s1 in states:
        for s2 in states:
            if (s1 in final_states and s2 not in final_states) or (s1 not in final_states and s2 in final_states):
                pair = (min(s1, s2), max(s1, s2))
                distinguishable[pair] = True
    
    # Step 3: Iteratively mark distinguishable pairs
    changed = True
    while changed:
        changed = False
        for (s1, s2) in state_pairs:
            if distinguishable[(s1, s2)]:
                continue
            for symbol in alphabet:
                t1 = transitions[s1][symbol]
                t2 = transitions[s2][symbol]
                if t1 != t2:
                    pair = (min(t1, t2), max(t1, t2))
                    if distinguishable.get(pair, False):
                        distinguishable[(s1, s2)] = True
                        changed = True
                        break

    # Step 4: Group equivalent states
    equivalent_states = defaultdict(set)
    for s1, s2 in state_pairs:
        if not distinguishable[(s1, s2)]:
            equivalent_states[s1].add(s2)
            equivalent_states[s2].add(s1)

    for state in states:
        equivalent_states[state].add(state)

    # Step 5: Build the minimized DFA by merging equivalent states
    merged_states = {}
    for state, equivalent_group in equivalent_states.items():
        # We merge states based on their equivalent group, using the first state in the group as the representative
        merged_states[state] = min(equivalent_group)

    # Step 6: Prepare the minimized DFA
    minimized_states = set(merged_states.values())
    minimized_start_state = merged_states[start_state]
    minimized_final_states = {merged_states[s] for s in final_states}
    minimized_transitions = {}

    for state in minimized_states:
        minimized_transitions[state] = {}
        for symbol in alphabet:
            # Use the representative state to find the next state
            representative_state = state
            next_state = transitions[representative_state][symbol]
            minimized_transitions[state][symbol] = merged_states[next_state]

    # Display the minimized DFA
    print("Minimized DFA:")
    print("States:", minimized_states)
    print("Start State:", minimized_start_state)
    print("Final States:", minimized_final_states)
    print("Transitions:")
    for state, trans in minimized_transitions.items():
        print(f"  {state}: {trans}")

# Example DFA
states = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'}
alphabet = {'a', 'b'}
transitions = {
    'A': {'a': 'B', 'b': 'F'},
    'B': {'a': 'G', 'b': 'C'},
    'C': {'a': 'A', 'b': 'C'},
    'D': {'a': 'C', 'b': 'C'},
    'E': {'a': 'H', 'b': 'F'},
    'F': {'a': 'C', 'b': 'G'},
    'G': {'a': 'G', 'b': 'E'},
    'H': {'a': 'C', 'b': 'C'}
}
start_state = 'A'
final_states = {'C'}

# Run the minimization
minimize_dfa(states, alphabet, transitions, start_state, final_states)
