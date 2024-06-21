import random
import itertools


class ProgramGenerator:
    def __init__(self, variables: set[str] = set()):
        self.variables = variables
        self.actions: dict[int, list[tuple[str, list[str]]]] = {
            0: [("SET", []), ("NOP", [])],
            1: [
                ("YIELD", ["var"]),
                ("INPUT", ["var"]),
                ("MULTI", ["cob", "cmd", "cse", "cmd", "ccb"]),
            ],
            2: [
                ("COPY", ["var", "var"]),
                ("IF", ["var", "cmp", "var", "cob", "cmd", "ccb"]),
                ("IF", ["var", "cmp", "var", "cob", "cmd", "cse", "cmd", "ccb"]),
                ("LOOP", ["var", "var", "cob", "cmd", "ccb"]),
                ("ADD", ["var", "var"]),
                ("SUB", ["var", "var"]),
                ("MUL", ["var", "var"]),
                ("DIV", ["var", "var"]),
                ("MOD", ["var", "var"]),
                ("POW", ["var", "var"]),
            ],
            3: [
                ("ADD", ["var", "var", "var"]),
                ("SUB", ["var", "var", "var"]),
                ("MUL", ["var", "var", "var"]),
                ("DIV", ["var", "var", "var"]),
                ("MOD", ["var", "var", "var"]),
                ("POW", ["var", "var", "var"]),
            ],
        }

    def generate_action(self, max_variables, blacklist):
        return random.choice(
            list(
                itertools.chain(
                    *[
                        filter(lambda x: x[0] not in blacklist, self.actions[x])
                        for x in self.actions.keys()
                        if x <= max_variables
                    ]
                )
            )
        )

    def generate_line(self, depth=0):
        action, arg_types = self.generate_action(
            len(self.variables), ["SET"] if depth > 0 else []
        )

        if action == "SET":
            var_name = f"v{len(self.variables)}"

            line = f"{action} {var_name} {self.generate_variable_start()}"

            self.add_variable(var_name)

        else:
            args = []

            for arg_type in arg_types:
                if arg_type == "var":
                    args.append(self.generate_argument())
                elif arg_type == "cmd":
                    args.extend(self.generate_line(depth + 1).split())
                elif arg_type == "cob":
                    args.append("(")
                elif arg_type == "cse":
                    args.append(";")
                elif arg_type == "ccb":
                    args.append(")")
                elif arg_type == "cmp":
                    args.append(random.choice([">", ">=", "=", "<=", "<", "!="]))

            line = f"{action} {' '.join(args)}"

        return line

    def generate_variable_start(self):
        return random.randrange(1, 10)

    def generate_program(self, num_lines):
        program = ""
        for _ in range(num_lines):
            program += self.generate_line() + "\n"

        self.variables = set()

        program = program[:-1]

        return program

    def add_variable(self, var_name):
        self.variables.add(var_name)

    def generate_argument(self):
        return random.choice(list(self.variables))


if __name__ == "__main__":
    generator = ProgramGenerator()

    print(generator.generate_program(20))
