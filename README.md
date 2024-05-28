# phenyo

Pinoy Henyo (a Filipino word guessing game, basically) implemented using genetic algorithm.

To run phenyo:
```
python phenyo.py [word]
```
where `[word]` is a string composed of only uppercase or lowercase letters.

## Dependencies

* `tabulate`

* `matplotlib`

## Specifics

*Crossover method*: $k$-point crossover (where $k$ is random, and the crossover points are at $len(\text{word}) / k$)

*Mutation method*: Simple mutation by randomly adding values from $-2$ to $2$ to one to three randomly selected letters.
