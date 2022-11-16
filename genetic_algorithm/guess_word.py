#  "DEAP Examples" (c) by R8V.
#  "DEAP Examples" is licensed under a
#  Creative Commons Attribution 4.0 International License.
#  You should have received a copy of the license along with this
#  work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
import array
import functools
import random
import string

from deap import base, creator


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
    alphabet = string.ascii_letters
    try:
        the_toolbox.attr_bool
    except AttributeError:
        the_toolbox.register("attr_bool", random.choice, alphabet)
    return the_toolbox.attr_bool

