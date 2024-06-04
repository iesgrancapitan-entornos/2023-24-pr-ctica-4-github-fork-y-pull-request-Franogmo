"""
Goal:
By Fran Ogallas
Start: Last update:
"""
import functools
from collections.abc import Iterator
from typeguard import typechecked


"""
BRAINSTORM. MOST OF THESE WILL END UP BEING GEN FUNCTIONS OR LAMBDAS
- Infinite iterator (DONE)
- Returns perfect numbers up to a limit (or up to infinity, if there is no set limit) (DONE)
- Returns all numbers ended in a given cypher between two numbers (If there is only one parameter, 
the 1st number will be 0) (DONE)
- Remake range().
- (GEN) Remake for each in range?
- (LAM) Returns the "sum" of a list of bools. In this "sum", Trues are considered 1's and Falses, -1's.
"""

class PerfectIterator(Iterator):

    def __init__(self, limit=None):
        self.n = 0
        self.__limit = limit

    def __next__(self):
        self.n = self.__next_perfect_n(self.n)
        if self.__limit is not None and self.n > self.__limit:
            raise StopIteration
        return self.n

    def __is_perfect(self, number):
        perfect_detection_tool = 0
        if number == 0 or number == 1:
            return False
        else:
            for n in range(1, number):
                if (number % n) == 0:
                    perfect_detection_tool = perfect_detection_tool + n
            if perfect_detection_tool == number:
                return True
            else:
                return False

    def __next_perfect_n(self, number):
        next_perfect_number = number
        while True:
            next_perfect_number += 1
            if self.__is_perfect(next_perfect_number):
                return next_perfect_number


@typechecked
class GivenEndIterator(Iterator):

    def __init__(self, given_end: int, limit1: int, limit2 = None):
        if given_end < 0 or given_end > 9:
            raise ValueError("The given end must have only 1 cypher.")
        else:
            self.__given_end = given_end
        self.__limit1 = limit1
        self.__limit2 = limit2
        if self.__limit2 is None:
            self.n = -1
        else:
            self.n = limit1 - 1

    def __next__(self):
        self.n = self.__next_candidate(self.n)
        if self.__limit2 is None and self.n > self.__limit1:
            raise StopIteration
        elif self.__limit2 is not None and self.n > self.__limit2:
            raise StopIteration
        return self.n

    def __next_candidate(self, number):
        while True:
            number += 1
            if number % 10 == self.__given_end:
                return number


def rhyme(rhyme, limit1, limit2 = None):
    if limit2 is None:
        pointer = -1
        end = limit1
    else:
        pointer = limit1 - 1
        end = limit2
    while pointer <= end:
        pointer += 1
        if pointer % 10 == rhyme:
            yield pointer


def main():
    print("Test 1 - Iterador de perfectos:")
    test1 = PerfectIterator(500)
    for n in test1:
        print(n)
    print("Test 2 - Iterador de finales (solo param de cierre):")
    test2 = GivenEndIterator(5, 50)
    for n in test2:
        print(n)
    print("Test 3 - Iterador de finales (ambos params):")
    test3 = GivenEndIterator(5, 100, 200)
    for n in test3:
        print(n)
    test_list1 = [173, 472, 14, 170, 266, 136, 227]
    test_lambda1 = lambda x: True if x%2==0 else False
    print("Test 4 - Pares True, Impares False:")
    test4 = list(map(test_lambda1, test_list1))
    print(test4)
    bool_to_one = lambda x: 1 if x else -1
    test_lambda2 = lambda x, y: x + bool_to_one(y)
    print("Test 5 - Sumatorio booleano en el que True = 1 y False = -1:")
    test5 = functools.reduce(test_lambda2, test4, 0)
    print(test5)
    print("Test 6 - Generador de finales:")
    for n in rhyme(8, 1000, 1090):
        print(n)








if __name__ == "__main__":
    main()