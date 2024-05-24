# phenyo

Pinoy Henyo (a Filipino word guessing game, basically) implemented using genetic algorithm.

To run phenyo:
```
./phenyo.py [N] [word]
```
where `[N]` represents the number of generations to run the algorithm.

## Dependencies

* `tabulate`

* `matplotlib`

## Specifics

*Crossover method*: $k$-point crossover (where $k$ is random, and the crossover points are at $len(\text{word}) / k$)

*Mutation method*: Simple mutation by randomly adding values from $-2$ to $2$ to one to three randomly selected letters.
