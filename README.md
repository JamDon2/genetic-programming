# Genetic Programming

```
########
#  ^ ^ #    ~.....................................~
 #  -   #   | Hi! Welcome to Genetic Programming! |
  #      #  | I will help you walk through this.  |
  ########  ~.....................................~
      \
     /  \
```

### PRs are welcome

## What is this?

This is a project which aims to evolutionarily (is that a word?) generate programs to meet specific criteria.

Or it throws together random stuff (smartly) until it works.

## How to use this?

Start `main.py` (`python main.py` or `python3 main.py`), and fill in the parameters.

You will need to provide some tasks that will have to be solved by the program. The inputs are given to it, and if they match the outputs you gave, it passes that test.

You will see `Best of generation n` and three numbers. The generations are the cycles in which the programs slowly improve, and the three numbers are the scores for the top three programs.

You should expect to see roughly `100 * number of tests` as a score, minus some value.

So if you see 570 as a score, it means that the program passed 6 tests.

The programs are stored in the `outputs/` folder.

You can run a program with `gc_interpreter.py program_name.gc`. If the program needs inputs, you will need to enter them one by one, one on each line.

## How does this work?

The system generates 10,000 (configurable) random programs in a custom programming language and stores them in a list. This is the _population_, and the first _generation_.

Each program is tested against a set of test cases, and based on the results and some other variables (length, complexity) each one gets assigned a _fitness score_, which can be used to rank them.

Once the programs are ranked, we have to create the next generation, which is hopefully a bit smarter on average, or in other words, has a higher average fitness score. To achieve this, we use three sources create it: top performing programs from the previous generation, random programs from the previous generation, and new, randomly generated programs.

These programs are then _mutated_ (meaning changed). Currently there are a few possible mutations:

-   adding a new random line in a random location
-   removing a random line
-   changing a random line, which has these sub-actions:
    -   replacing the line entirely
    -   changing the inner command, while keeping the outer intact
    -   popping out the inner command (removing the outer)

Once the new population is ready, the process gets repeated.

The best program of each generation gets saved in the outputs folder.

## How do I use this? (Advanced)

First, write your tests in `gc_tests.py` (use `gc_tests.example.py` as a guide). The first array in each tuple are the inputs (there can be multiple), and the second are the expected outputs (it can also have multiple).

After that, you can run `gc_evolution.py`.

You'll see the fitness scores of the top three programs (one test passed is 100 points, so anything above `n * 100` should be roughly `n + 1` tests passed).

Here is what you can (and should) tweak:

-   Magic values at the top of the file
-   The `static_fitness` function
-   Population size at the bottom in the call to `create_population`

Of course, once you look through the code you can edit anything you want, these are just the easiest places to start.
