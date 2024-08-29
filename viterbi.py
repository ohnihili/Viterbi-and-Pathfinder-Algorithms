import sys
import numpy as np

input_file = sys.argv[1]
grid_map = []
obs_sequences = []
num_obs = 0

# Read input file
with open(input_file, 'r') as file:
    rows, cols = map(int, file.readline().split())
    for i in range(rows):
        line = file.readline().split()
        grid_map.append(line)
    num_obs = int(file.readline())
    for j in range(num_obs):
        obs_sequences.append(str(file.readline().strip()))
    error_probability = float(file.readline())

states = []
state_transitions = []
adjacent_cells = []
num_states = 0
movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Process grid map and identify states
for i in range(rows):
    for j in range(cols):
        if grid_map[i][j] == "0":
            grid_map[i][j] = num_states
            states.append((i, j))
            state_transitions.append([1, 1, 1, 1])
            neighbors = [(), (), (), ()]
            index = 0
            for move in movements:
                neighbor = (i + move[0], j + move[1])
                neighbors[index] = neighbor
                r, c = neighbor
                is_valid = 0 <= r < rows and 0 <= c < cols and grid_map[r][c] != 'X'
                if is_valid:
                    state_transitions[-1][index] = 0
                index += 1
            adjacent_cells.append(neighbors)
            num_states += 1

initial_probability = 1 / num_states
state_probabilities = [initial_probability for _ in range(num_states)]

# Initialize transition matrix
transition_probabilities = [[0 for _ in range(num_states)] for _ in range(num_states)]
for i in range(num_states):
    count = sum(1 for x in state_transitions[i] if x == 0)
    for j in range(4):
        if state_transitions[i][j] == 0:
            r, c = adjacent_cells[i][j]
            transition_probabilities[i][grid_map[r][c]] = 1 / count

# Initialize emission matrix
emission_probabilities = [[0 for _ in range(num_obs)] for _ in range(num_states)]
for i in range(num_states):
    for j in range(num_obs):
        count = sum(1 for k in range(4) if state_transitions[i][k] == int(obs_sequences[j][k]))
        emission_probabilities[i][j] = ((1 - error_probability) ** count) * (error_probability ** (4 - count))

# Initialize trellis for dynamic programming
trellis = [[0 for _ in range(num_obs)] for _ in range(num_states)]
for i in range(num_states):
    trellis[i][0] = state_probabilities[i] * emission_probabilities[i][0]

# Fill in the trellis
for j in range(1, num_obs):
    for i in range(num_states):
        max_prob = -1
        for k in range(num_states):
            prob = trellis[k][j - 1] * transition_probabilities[k][i] * emission_probabilities[i][j]
            if prob > max_prob:
                max_prob = prob
        trellis[i][j] = max_prob

# Create trellis map for final output
trellis_output = [[[0 for _ in range(cols)] for _ in range(rows)] for _ in range(num_obs)]
for obs_idx in range(num_obs):
    for state_idx in range(num_states):
        r, c = states[state_idx]
        trellis_output[obs_idx][r][c] = trellis[state_idx][obs_idx]

# Save trellis output to file
np.savez("output.npz", *trellis_output)
