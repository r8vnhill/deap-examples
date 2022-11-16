#  "DEAP Examples" (c) by R8V.
#  "DEAP Examples" is licensed under a
#  Creative Commons Attribution 4.0 International License.
#  You should have received a copy of the license along with this
#  work. If not, see <https://creativecommons.org/licenses/by/4.0/>.

import array
import functools
import random

import numpy
from deap import algorithms, base, creator, tools


def get_optimizer() -> base.Fitness:
    try:
        creator.FitnessMax
    except AttributeError:
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    return creator.FitnessMax


def individual_creator() -> array.array:
    try:
        creator.Individual
    except AttributeError:
        creator.create("Individual", array.array, typecode='b', fitness=get_optimizer())
    return creator.Individual


def attribute_generator(the_toolbox: base.Toolbox) -> functools.partial:
    try:
        the_toolbox.attr_bool
    except AttributeError:
        the_toolbox.register("attr_bool", random.randint, 0, 1)
    return the_toolbox.attr_bool


def individual_initializer(the_toolbox: base.Toolbox) -> functools.partial:
    try:
        the_toolbox.individual
    except AttributeError:
        the_toolbox.register("individual", tools.initRepeat, individual_creator(),
                             attribute_generator(the_toolbox), 100)
    return the_toolbox.individual


def population_initializer(the_toolbox: base.Toolbox) -> functools.partial:
    try:
        the_toolbox.population
    except AttributeError:
        the_toolbox.register("population", tools.initRepeat, list,
                             individual_initializer(the_toolbox))
    return the_toolbox.population


toolbox = base.Toolbox()


def count_ones(individual):
    return sum(individual),


toolbox.register("evaluate", count_ones)
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
    _, _, fittest = main()
    print(fittest[0])
