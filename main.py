from typing import Literal
from time import sleep
import os

CHARACTERS = {
    "INFO": """########  
#  ^ ^ #  
 #  -   # 
  #      #
  ########
      \   
     /  \ """,
    "ERROR": """########  
#  O O #  
 #  -   # 
  #      #
  ########
      \   
     /  \ """,
}

CHARACTER_STYLES = {"INFO": "2m", "ERROR": "2;31m"}


ESCAPE = chr(27) + "["

RESET = ESCAPE + "0m"


def wrap_escape(text: str, escape: str) -> str:
    return ESCAPE + escape + text + RESET


def create_text_box(text: str) -> list[str]:
    lines = text.split("\n")

    longest_line = max([len(line) for line in lines])

    side = "~" + "." * (longest_line + 2) + "~"

    result_lines = []

    result_lines.append(side)

    for line in lines:
        padding_amount = longest_line - len(line)
        result_lines.append("| " + line + " " * padding_amount + " |")

    result_lines.append(side)

    return result_lines


def print_message(
    text: str,
    offset: int,
    print_type: Literal["INFO", "ERROR"] = "INFO",
):
    box = create_text_box(text)

    base = CHARACTERS[print_type]

    lines = base.split("\n")

    for i, box_line in enumerate(box):
        while len(lines) - 1 < i + offset:
            lines.append(" " * len(lines[0]))

        lines[i + offset] += "  " + box_line

    print(wrap_escape("\n".join(lines), CHARACTER_STYLES[print_type]))


print()

print_message("Welcome to Genetic Programming!\nLet's set everything up.", 1)

print()

print(wrap_escape("  How many tasks would you like to add?", "1m"))
try:
    tests_number = input("> " + ESCAPE + "33m")
except KeyboardInterrupt:
    print(RESET + "\nBye.")
    exit()

print(RESET + "\n")

try:
    tests_number = int(tests_number)
except ValueError:
    print_message("That doesn't look like a number!", 1, "ERROR")
    exit()


print(wrap_escape("Okay, let's see them!", "1m"))

print()

print(
    wrap_escape(
        "Each program can take multiple inputs and multiple outputs, but the more you add, the harder it will be for it find a solution.",
        "2m",
    )
)

print()

print(
    wrap_escape(
        "Provide them in this format: INPUT0 INPUT1 = OUTPUT1 OUTPUT2 OUTPUT3\nFor example: 1 2 = 3 - this would be a program which adds the two inputs.",
        "2m",
    )
)

print()

tests = []

for i in range(tests_number):
    try:
        test = input(
            f"{str(i+1).zfill(len(str(tests_number)))}/{tests_number} > "
            + ESCAPE
            + "33m"
        )
    except KeyboardInterrupt:
        print(RESET + "\nBye.")
        exit()

    test = test.split("=")

    if len(test) != 2:
        print("\n")
        print_message("Hmm... I don't understand that.", 1, "ERROR")
        exit()

    try:
        test = [[int(value) for value in x.strip().split(" ")] for x in test]
    except ValueError:
        print("\n")
        print_message("Hmm... I don't understand that.", 1, "ERROR")
        exit()

    tests.append(test)

    print(RESET)

print_message("Great, I'll start the evolution now!", 1)

sleep(2)

print()


from gc_evolution import (
    create_population,
    Interpreter,
    Runner,
    evaluate_population,
    reproduce,
    mutate,
)

population = create_population(10000)

generation = 0

interpreter = Interpreter(False)

runner = Runner(interpreter)

runner.create_workers(1)

if not os.path.exists("outputs"):
    os.mkdir("outputs")

while True:
    population, fitness_scores = evaluate_population(population, runner, tests)

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
