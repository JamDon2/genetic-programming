import math
import random

from gc_generator import ProgramGenerator
from gc_interpreter import Interpreter
from gc_utils import random_inverse_square, run_program_timeout, get_variables


def create_population(n=100, length_function=lambda: int(random_inverse_square() * 3)):
    generator = ProgramGenerator()
    return [generator.generate_program(length_function()) for x in range(n)]


def evaluate_population(population, fitness_function):
    fitness_scores = [fitness_function(program) for program in population]

    return [
        program
        for _, program in sorted(
            zip(fitness_scores, population),
            reverse=True,
        )
    ], sorted(fitness_scores, reverse=True)


def fitness(program: str):
    fitness_score = 0

    if len(program.split("\n")) > 10:
        fitness_score -= len(program.split("\n")) * 3
    else:
        fitness_score -= len(program.split("\n"))
        fitness_score -= len(program) // 5

    interpreter = Interpreter(False)

    tests = [
        [[1], [9]],
        [[8], [4]],
        [[9], [9]],
        [[4], [4]],
        [[3], [9]],
        [[6], [4]],
        [[77], [9]],
    ]

    yield_target = 1
    input_target = 1

    fitness_score -= abs(yield_target - program.count("YIELD")) * 4
    fitness_score -= abs(input_target - program.count("INPUT")) * 4

    tests_passed = 0

    pass_index = None

    for test in tests:
        try:
            result = run_program_timeout(interpreter, program, test[0])
        except:
            break

        # if pass_index is None:
        #     try:
        #         pass_index = result.index(test[1])
        #     except:
        #         pass

        # if (
        #     pass_index is None
        #     or len(result) <= pass_index
        #     or result[pass_index] != test[1]
        # ):
        #     break

        if result != test[1]:
            break

        tests_passed += 1

    fitness_score += tests_passed * 100

    return fitness_score


def mutate(program: str):
    should_mutate = random.random() > 0.3

    if not should_mutate:
        return program

    program_lines = program.split("\n")

    action = random.choices(["add_line", "remove_line", "modify_line"], [3, 1, 2])[0]

    while len(program_lines) == 1 and action == "remove_line":
        action = random.choices(["add_line", "remove_line", "modify_line"], [3, 1, 2])[
            0
        ]

    line = random.randint(0, program.count("\n"))

    old_line = program_lines[line].split()

    if len(old_line) == 0:
        print(program_lines)
        print(line, old_line, action)

    while (
        action in ["remove_line", "modify_line"]
        and old_line[0] == "SET"
        and program.count(old_line[1]) > 1
    ):
        action = random.choices(["add_line", "remove_line", "modify_line"], [3, 1, 2])[
            0
        ]
        line = random.randint(0, program.count("\n"))
        old_line = program_lines[line].split()

    variables = get_variables("\n".join(program_lines[:line]))

    generator = ProgramGenerator(variables)

    new_line = generator.generate_line().split()

    if new_line[0] == "SET":
        new_line[1] = f"v{max([int(var[1:]) for var in get_variables(program)]) + 1}"

    new_line = " ".join(new_line)

    if action == "add_line":
        program_lines.insert(line, new_line)
    elif action == "remove_line":
        program_lines.pop(line)
    elif action == "modify_line":
        program_lines[line] = new_line

    should_mutate_again = random.random() < 0.6

    result = "\n".join(program_lines)

    if should_mutate_again:
        return mutate(result)

    return result


def reproduce(
    population: list[str],
    mutation_function,
    survive_top=0.25,
    survive_random=0.1,
    new_random=0.25,
):
    survived_top = math.ceil(len(population) * survive_top)
    survived_random = math.ceil(len(population) * survive_random)
    new_programs = math.ceil(len(population) * new_random)

    reproducing_programs = population[:survived_top] + random.sample(
        population[survived_top:], survived_random
    )

    new_population = []

    for i in range(len(population) - new_programs):
        new_population.append(
            mutation_function(reproducing_programs[i % len(reproducing_programs)])
        )

    new_population.extend(create_population(new_programs))

    return new_population


population = create_population(10000)

generation = 0

while True:
    population, fitness_scores = evaluate_population(population, fitness)

    print(
        f"Best of generation {generation}:",
        fitness_scores[0],
        fitness_scores[1],
        fitness_scores[2],
    )

    with open(f"outputs/g{generation}.gc", "w") as f:
        f.write(population[0])

    population = reproduce(population, mutate)

    generation += 1