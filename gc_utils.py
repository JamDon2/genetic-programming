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


class Runner:
    def __init__(self, interpreter: Interpreter) -> None:
        self.interpreter = interpreter
        self.worker = None
        self.task_queue = None
        self.output_queue = None

    def work(self) -> None:
        while True:
            code, inputs = self.task_queue.get(True)
            start = time.time()
            try:
                result = self.interpreter.run(code, inputs, timeout=0.1)
                end = time.time()
                self.output_queue.put((result, end - start))
            except:
                self.output_queue.put((None, None))

    def create_worker(self, replace=False) -> None:
        if not replace and self.worker:
            return

        if self.worker:
            self.worker.kill()

        self.task_queue, self.output_queue = Queue(), Queue()

        self.worker = Process(target=self.work, args=())

        self.worker.start()

    def run(self, code: str, inputs: list[int] = []) -> tuple[list[int], int]:
        self.create_worker()

        self.task_queue.put((code, inputs))

        return self.output_queue.get(True)

    def queue(self, code: str, inputs: list[int] = []) -> None:
        self.task_queue.put((code, inputs))

    def queue_many(self, programs: list[str], inputs: list[int] = []) -> None:
        for program in programs:
            self.task_queue.put((program, inputs))

    def get(self, amount: int) -> list[tuple[list[int], int]]:
        outputs = []

        while len(outputs) < amount:
            outputs.append(self.output_queue.get(timeout=0.1))

        return outputs
