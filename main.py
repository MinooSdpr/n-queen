"""
N-Queens Solver Using Genetic Algorithm with Tkinter GUI

This Python program solves the N-Queens problem using a Genetic Algorithm
and displays the result in a graphical chessboard interface using Tkinter.

Features:
- Allows user input for:
    - Board size (between 4 and 10)
    - Population size (positive integer)
    - Mutation rate (float between 0 and 1)
- Solves the problem using a Genetic Algorithm.
- Visualizes the final solution on a chessboard.
- Displays the generation number in which a valid solution was found.
- Handles input validation gracefully and shows helpful error messages.

Limitations:
- The board visualization is limited to sizes ≤ 10 for clarity and performance.
- If no perfect solution is found within `2 × N` generations, the best result is shown.

Modules Used:
- tkinter: for GUI interface and board rendering.
- random: for generating and mutating population members.

Author: Minoo Sayyadpour
Date: 2025-07-05
"""

from tkinter import *
from random import randint, shuffle


def build_population(population_size, n):
    """Generate a population of random individuals, each a list of length n with values in [0, n-1]."""
    return [[randint(0, n - 1) for _ in range(n)] for _ in range(population_size)]

def crossover(population_list, n):
    """Crossing pairs in the population at the midpoint, doubling population size."""
    div_index = n // 2
    new_population = population_list.copy()
    for i in range(0, len(population_list) - 1, 2):
        child1 = population_list[i][:div_index] + population_list[i + 1][div_index:]
        child2 = population_list[i + 1][:div_index] + population_list[i][div_index:]
        new_population.extend([child1, child2])
    return new_population

def mutation(population_list, mutation_rate, n):
    """Randomly mutate a subset of the second half of the population based on mutation_rate."""
    mutated_population = list(range(len(population_list) // 2, len(population_list)))
    shuffle(mutated_population)
    chosen_ones = mutated_population[:int(len(mutated_population) * mutation_rate)]
    for i in chosen_ones:
        col = randint(0, n - 1)
        val = randint(0, n - 1)
        population_list[i][col] = val
    return population_list

def evaluate_gen(gen):
    """Calculate the number of conflicts of queens (attacking pairs) in a board."""
    conflict = 0
    for i in range(len(gen)):
        for j in range(i + 1, len(gen)):
            if gen[i] == gen[j] or abs(i - j) == abs(gen[i] - gen[j]):
                conflict += 1
    return conflict

def fitness(population_list):
    """Return a list of conflict counts for each boards in the population."""
    return [evaluate_gen(individual) for individual in population_list]

def eliminate(population_list, evaluate_list, population_size):
    """Select the top boards with the lowest conflicts up to population_size;
        return early if a perfect board (0 conflicts) is found."""
    combined = sorted(zip(evaluate_list, population_list), key=lambda x: x[0])
    if combined[0][0] == 0:
        return [combined[0][1]], [0]
    top = combined[:population_size]
    return [p for _, p in top], [e for e, _ in top]

# --- GUI Functions ---

def clear_board():
    canvas.delete("all")


def draw_board(answer, generation):
    """
    Draw an n x n chessboard and place queens according to the solution 'answer'.

    Args:
        answer (list): List where index is row and value is the column of the queen.
        generation (int or None): Generation number if a perfect solution was found; None otherwise.

    This function clears the existing board, draws alternating colored tiles,
    and places red queen symbols where indicated by 'answer'.
    Updates a label with the generation info or a message if no perfect solution exists.
    """
    clear_board()
    n = len(answer)
    tile_size = 480 // n
    colors = ["#f5f5f5", "#100c08"]

    for row in range(n):
        for col in range(n):
            x1, y1 = col * tile_size, row * tile_size
            x2, y2 = x1 + tile_size, y1 + tile_size
            color = colors[(row + col) % 2]  # Alternate colors for board tiles
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

            if answer[row] == col:
                # Place queen symbol at the center of the tile
                canvas.create_text(
                    x1 + tile_size // 2,
                    y1 + tile_size // 2,
                    text="♛",
                    font=("Arial", tile_size // 2),
                    fill="#c4aead"
                )

    # Update result label with generation info or fallback message
    if generation is not None:
        result_label.config(text=f"✅ Solution found in generation: {generation}")
    else:
        result_label.config(text="⚠️ No perfect solution found. Showing best attempt.")


def start_algorithm():
    """
    Initialize parameters from GUI input and run the genetic algorithm for N-Queens.

    Validates inputs, runs the algorithm for a fixed number of generations,
    and updates the board with the best solution or a perfect solution if found.
    Handles invalid inputs by showing error messages.
    """
    try:
        n = int(entry_n.get())  # Board size
        pop_size = int(entry_pop.get())
        mut_rate_str = entry_mut.get()
        mut_rate = float(mut_rate_str)

        if n < 4 or n > 10:
            result_label.config(text="❌ Board size must be between 4 and 10")
            return

        if pop_size <= 0 or pop_size > 500:
            result_label.config(text="❌ Population size must be between 1 and 500")
            return

        if not (0 <= mut_rate <= 1):
            result_label.config(text="❌ Mutation rate must be between 0 and 1")
            return

        if len(mut_rate_str.split('.')[-1]) > 2:
            result_label.config(text="❌ Mutation rate must have at most 2 decimal places")
            return

        generations = n * 2  # Set max generations proportional to board size
        population = build_population(pop_size, n)

        for gen in range(generations):
            population = crossover(population, n)
            population = mutation(population, mut_rate, n)
            scores = fitness(population)
            population, scores = eliminate(population, scores, pop_size)

            if 0 in scores:
                draw_board(population[0], gen + 1)
                return

        draw_board(population[0], None)

    except ValueError:
        result_label.config(text="❌ Please enter valid numbers.")


# --- GUI Setup ---

root = Tk()
root.title("N-Queens Genetic Algorithm")
root.minsize(485, 660)
# Inputs
Label(root, text="Board Size (4–10):").grid(row=0, column=0, sticky=E, padx=5, pady=5)
entry_n = Entry(root)
entry_n.insert(0, "8")
entry_n.grid(row=0, column=1)

Label(root, text="Population Size:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
entry_pop = Entry(root)
entry_pop.insert(0, "50")
entry_pop.grid(row=1, column=1)

Label(root, text="Mutation Rate (0–1):").grid(row=2, column=0, sticky=E, padx=5, pady=5)
entry_mut = Entry(root)
entry_mut.insert(0, "0.4")
entry_mut.grid(row=2, column=1)

Button(root, text="Start", command=start_algorithm, bg="lightgreen").grid(row=3, columnspan=2, pady=10)

# Result message
result_label = Label(root, text="", fg="blue", font=("Arial", 12))
result_label.grid(row=4, columnspan=2)

# Chessboard canvas
canvas = Canvas(root, width=480, height=480, bg="white")
canvas.grid(row=5, columnspan=2, pady=10)

root.mainloop()
