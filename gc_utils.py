import random
import re
from multiprocessing import Process, Queue
import time

from gc_interpreter import Interpreter


def random_inverse_square():
    random_value = random.random()

    inverse_square_number = 1 / (random_value**0.5)

    return inverse_square_number


def get_variables(program):
    return set(re.findall("v[0-9]+", program))


def split_command(command: list[str]):
    nest_level = 0
    action_no = 0

    main = []

    commands = []

    for word in command:
        if word == ")":
            nest_level -= 1

            if nest_level == 0:
                continue

        if word == "(":
            nest_level += 1

            if nest_level == 1:
                if action_no != 0:
                    action_no += 1
                commands.append([])
                continue

        if word == ";" and nest_level == 1:
            action_no += 1
            commands.append([])
            continue

        if nest_level == 0:
            main.append(word)
        else:
            commands[action_no].append(word)

    return main, commands


def combine_command(main, commands):
    result = []

    result.extend(main)

    if len(commands) > 0:
        result.append("(")

        for i, command in enumerate(commands):
            result.extend(command)

            if i != len(commands) - 1:
                result.append(";")

        result.append(")")

    return result


class AlreadyExistsException(Exception):
    pass


def work(interpreter: Interpreter, task_queue: Queue, output_queue: Queue) -> None:
    while True:
        code, inputs, program_id, test_id = task_queue.get(True)
        start = time.time()
        try:
            result = interpreter.run(code, inputs, timeout=0.1)
            end = time.time()
            output_queue.put((result, end - start, program_id, test_id))
        except:
            output_queue.put((None, None, program_id, test_id))


class Runner:
    def __init__(self, interpreter: Interpreter) -> None:
        self.interpreter = interpreter
        self.workers = []
        self.task_queue = None
        self.output_queue = None
        self.results: dict[int, tuple[list[int], int]] = {}
        self.queued = 0

    def create_workers(self, amount=1) -> None:
        if len(self.workers) > 0:
            raise AlreadyExistsException()

        self.task_queue = Queue()
        self.output_queue = Queue()

        for i in range(amount):
            self.workers.append(
                Process(
                    target=work,
                    args=(self.interpreter, self.task_queue, self.output_queue),
                )
            )

        for worker in self.workers:
            worker.start()

    def kill_workers(self) -> None:
        for worker in self.workers:
            worker.kill()

        self.workers = []

    def queue_test(self, programs: list[tuple[str, int]], test: list[int]) -> None:
        for program_id, (program, program_id) in enumerate(programs):
            self.task_queue.put((program, test, program_id))
            self.queued += 1

    def collect_results(self) -> None:
        self.results = {}

        for i in range(self.queued):
            results, runtime, program_id = self.output_queue.get(timeout=0.2)

            self.results[program_id] = (results, runtime)

        self.queued = 0

    def get_program_results(self, program_id: int) -> dict[int, tuple[list[int], int]]:
        return self.results[program_id]
