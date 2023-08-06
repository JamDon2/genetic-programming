import random
import re
from timeout_decorator import timeout

from gc_interpreter import Interpreter


def random_inverse_square():
    random_value = random.random()

    inverse_square_number = 1 / (random_value**0.5)

    return inverse_square_number


def get_variables(program):
    return set(re.findall("v[0-9]+", program))


@timeout(0.01)
def run_program_timeout(interpreter: Interpreter, code: str, inputs: list[int] = []):
    return interpreter.run(code, inputs)
