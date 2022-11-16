#  "DEAP Examples" (c) by R8V.
#  "DEAP Examples" is licensed under a
#  Creative Commons Attribution 4.0 International License.
#  You should have received a copy of the license along with this
#  work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
import array
import functools
import random
import re
import string

import numpy
from deap import algorithms, base, creator, tools


def get_optimizer() -> base.Fitness:
    """
    The optimization strategy is to maximize the fitness.
    """
    try:
        creator.fitness_max
    except AttributeError:
        creator.create("fitness_max", base.Fitness, weights=(1.0,))
    return creator.fitness_max


def individual_creator() -> array.array:
    """
    The individual creator.
    """
    try:
        creator.individual_creator
    except AttributeError:
        creator.create("individual_creator", array.array, fitness=get_optimizer())
    return creator.individual_creator


def attribute_generator(the_toolbox: base.Toolbox) -> functools.partial:
    """
    The attribute generator.
    It chooses a random character from the string of ASCII characters.
    """
    res = list(re.sub('.', lambda x: r'\u % 04X' % ord(x.group()), string.printable))

    try:
        the_toolbox.attr_bool
    except AttributeError:
        the_toolbox.register("attr_bool", random.choice, res)
    return the_toolbox.attr_bool


def individual_initializer(the_toolbox: base.Toolbox) -> functools.partial:
    try:
        the_toolbox.individual
    except AttributeError:
        the_toolbox.register("individual", tools.initRepeat, individual_creator(),
                             attribute_generator(the_toolbox), 10)
    return the_toolbox.individual


def population_initializer(the_toolbox: base.Toolbox) -> functools.partial:
    try:
        the_toolbox.population
    except AttributeError:
        the_toolbox.register("population", tools.initRepeat, list,
                             individual_initializer(the_toolbox))
    return the_toolbox.population


toolbox = base.Toolbox()

target: str


def count_matches(individual):
    """
    The fitness function.
    It counts the number of characters that match the target word.
    """
    return sum(1 for expected, actual in zip(target, individual) if expected == actual),


toolbox.register("evaluate", count_matches)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    pop = population_initializer(toolbox)(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40,
                                   stats=stats, halloffame=hof, verbose=True)

    return pop, log, hof


if __name__ == "__main__":
    target = "Sopaipilla"
    _, _, fittest = main()
    print(fittest[0])
