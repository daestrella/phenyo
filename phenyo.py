from tabulate import tabulate
import matplotlib.pyplot as plot
import random
import math
import string
import argparse

class NoMorePossibleGuessError(Exception):
    pass

class Guess:
    alphabet  = string.ascii_lowercase + string.ascii_uppercase
    history   = []
    cx_rate   = 0.80
    mn_counts = [   0,    1,    2,    3]
    mn_rates  = [4/10, 3/10, 2/10, 1/10]
    retries   = 5                            # attempts before giving up generating compatible words
    tolerance = 0.01

    def __init__(self, string=None):
        self.string = Guess.deviate(string) if string else Guess.generate_string()
        self.correctness = Checker.how_close_to_the_word(self.string)

    def is_fit_with(self, guess):
        '''Checks whether two guesses are compatible to each other, i.e.,
        correctness values are within the tolerated range with respect to time.'''
        # Tolerance decrease as time reaches Game.limit to ensure better guess
        if self.correctness == guess.correctness == 0:
            return True

        return self.correctness < (guess.correctness - 1 + (guess.correctness * Guess.tolerance / Game.attempt))

    @staticmethod
    def deviate(string):
        '''Add slight variation to the guess string through mutation.'''

        mutation_count = random.choices(Guess.mn_counts, weights=Guess.mn_rates, k=1)[0]

        if mutation_count == 0 or len(Checker.string) < 4:
            return string

        mutated_string = list(string)
        for _ in range(mutation_count):
            i = random.randint(0, len(string)-1)
            mutated_string[i] = chr(ord(mutated_string[i]) + random.randint(-2, 2))

        return ''.join(mutated_string)

    @staticmethod
    def generate_string():
        return ''.join(random.choices(Guess.alphabet, k=len(Checker.string)))
        
    @classmethod
    def infer_from_last_attempt(cls):
        '''Combine guesses from previous attempt through crossover.'''
        previous1, previous2 = Guess.history[-1]

        if (previous1.correctness == 0) or (previous2.correctness == 0):
            return previous1 if previous1.correctness == 0 else previous2

        if random.random() > Guess.cx_rate:
            return cls(previous1.string) if previous1.correctness < previous2.correctness else cls(previous2.string)
        
        string1, string2 = list(previous1.string), list(previous2.string)

        # k-point crossover (lower points = higher probability (1/(k+1)))
        try:
            for _ in range(Guess.retries):
                cx_num = random.choices([*range(1, len(Checker.string)+1)],
                                        weights=[1/(i+1) for i, _ in enumerate(Checker.string)],k=1)[0]

                for i in range(0, len(Checker.string), len(Checker.string)//cx_num):
                    if i == 0:
                        continue
                    string1, string2 = string1[:i] + string2[i:], string2[:i] + string1[i:]

                inference1, inference2 = cls(''.join(string1)), cls(''.join(string2))
                if min(inference1.correctness, inference2.correctness) < min(previous1.correctness, previous2.correctness):
                    break
            else:
                raise NoMorePossibleGuessError
        except NoMorePossibleGuessError:
            return previous1 if previous1.correctness < previous2.correctness else previous2

        return inference1 if inference1.correctness < inference2.correctness else inference2

    @classmethod
    def guess(cls):
        '''Returns best guess of the current attempt.'''
        if not Guess.history:   # attempt 1
            guess1, guess2 = cls(), cls()
            Guess.history.append([guess1, guess2])
            return guess1 if guess1.correctness < guess2.correctness else guess2
        
        guess1 = cls.infer_from_last_attempt()  # combine previous guesses
        
        try:
            for _ in range(Guess.retries):
                guess2 = cls()
                if guess2.is_fit_with(guess1):
                    break
            else:
                raise NoMorePossibleGuessError

        except NoMorePossibleGuessError:
            guess2 = guess1

        Guess.history.append([guess1, guess2])
        return guess1 if guess1.correctness < guess2.correctness else guess2

class Checker:
    @staticmethod
    def how_close_to_the_word(string):
        return sum((ord(string_char) - ord(game_char)) ** 2
                   for string_char, game_char in zip(string, Checker.string))

class Game:
    attempt = 0
    history = []

    @staticmethod
    def start(string):
        Checker.string = string

        Game.find_next()

        while Game.history[-1].correctness != 0:
            Game.find_next()

        Game.plot()
        plot.show()
        Game.show_history()

    @staticmethod
    def find_next():
        Game.attempt += 1
        if not Game.history:    # attempt 1
            Game.history.append(Guess.guess())
            return
        
        guess = Guess.guess()
        if guess.correctness < Game.history[-1].correctness:
            Game.history.append(guess)
        else:
            Game.history.append(Game.history[-1])
    
    @staticmethod
    def show_history():
        print(tabulate(
            [(i, guess.string, guess.correctness)
            for i, guess in enumerate(Game.history, start=1)],
            headers=['Generation', 'Best Guess', 'Cost Value'],
            tablefmt='simple')
              )
    
    @staticmethod
    def show_history():
        print(tabulate(
            [(i, guess.string, guess.correctness)
            for i, guess in enumerate(Game.history, start=1)],
            headers=['Generation', 'Best Guess', 'Cost Value'],
            tablefmt='simple')
              )

    @staticmethod
    def plot():
        '''plot fitness value from Game.history to generation number'''
        plot.clf()
        plot.plot(range(1, Game.attempt + 1), [best.correctness for best in Game.history], linestyle='-')
        plot.xlabel('Generation')
        plot.ylabel('Fitness value')
        plot.title(f'Genetic algorithm: word guessing (current: {Game.history[-1].correctness})')
        plot.grid(True)
        plot.draw()
        plot.pause(0.01)

def natural(value):
    if int(value) <= 0:
        raise argparse.ArgumentTypeError(f'{value} is not a positive integer!')
    return int(value)

def is_valid_string(string):
    return all(char.islower() or char.isupper() for char in string)

parser = argparse.ArgumentParser(description='Pinoy henyo guessing game')
parser.add_argument('word', type=str, help='the word to be guessed')

args = parser.parse_args()
Game.start(args.word)
