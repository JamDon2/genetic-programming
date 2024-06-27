# Genetic Programming

### PRs are welcome

## What is this?

This project is a combination of multiple things:

- a simplified, non-turing complete, assembly-like language
- a script that can generate programs in this language randomly
- the main script, an evolutionary algorithm, that selects for the best programs based on the fitness criteria

## How does it work?

The system generates 10,000 (configurable) random programs with random lengths (inverse square) and stores it. This is the population.

A fitness function tests each program according to the set test cases, and assigns a fitness based on that and other variables such as program length.

The programs are ranked based on score, and then programs are selected for reproduction with three methods: a percentage of the top performing programs, random programs from the population, newly generated random programs.

These programs are then mutated, and they replace the existing population.

## How do I use it?

First, write your tests in `gc_tests.py` (use `gc_tests.example.py` as a guide). The first array in each tuple are the inputs (there can be multiple), and the second are the expected outputs (it can also have multiple).

After that, you can run `gc_evolution.py`.

You'll see the fitness scores of the top three programs (one test passed is 100 points, so anything above `n * 100` should be roughly `n + 1` tests passed).

You can tweak the fitness function in gc_evolution.py for your use case.
