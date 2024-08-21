from functools import reduce


def main():
    q1()
    q2()
    print(q3([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    q4()
    print(q5([1, 2, 3, 4, 5, 6]))
    print(q6([["madam", "test", "level"], ["hello", "racecar", "world"], ["noon", "civic", "radar"]]))
    print(q8()([10, 3, 5, 8, 2, 11, 4, 7]))


def q1():
    fibonacci = lambda n: [0, 1][:n] if n <= 2 else fibonacci(n - 1) + [fibonacci(n - 1)[-1] + fibonacci(n - 2)[-1]]
    print(fibonacci(9))

def q2():
    concatenate = lambda lst: lst[0] if len(lst) == 1 else lst[0] + ' ' + concatenate(lst[1:])
    print(concatenate(["Hello", "world", "this", "is", "afik&gal"]))


def q3(lst):
    return list(map(lambda sublist: reduce(lambda cum_sum, x: cum_sum + x
                ,map(lambda y: y ** 2,filter(lambda z: z % 2 == 0,sublist)),0),lst))



def q4():
    def accumulate(binary_op):
        def inner(sequence):
            result = sequence[0]
            for i in range(1, len(sequence)):
                result = binary_op(result, sequence[i])
            return result

        return inner

    factorial = accumulate(lambda x, y: x * y)
    print(factorial([1, 2, 3, 4, 5]))

    exponentiation = accumulate(lambda x, y: x ** y)
    print(exponentiation([2, 3, 4]))


def q5(lst):
    return reduce(lambda x, y: x + y, map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, lst)))


def q6(lst):


    from functools import reduce

    return list(
        map(lambda sublist: reduce(lambda acc, word: acc + 1, filter(lambda word: word == word[::-1], sublist), 0),
            lst))


def q7():
    def generate_values():
        print('Generating values...')
        yield 1
        yield 2
        yield 3

    def square(x):
        print(f'Squaring {x}')
        return x * x

    # Eager evaluation:
    # In eager evaluation, the program generates all values from generate_values() immediately
    # and stores them in a list. Then it squares each value right away.

    print('Eager evaluation:')
    values = list(generate_values())
    squared_values = [square(x) for x in values]
    print(squared_values)

    # Lazy evaluation:
    # In lazy evaluation, the program generates each value from generate_values() only when it's
    # about to be used. It squares one value at a time as it's being generated, instead of doing
    # everything at once. This saves memory and processing time, especially with large data.

    print('\nLazy evaluation:')
    squared_values = [square(x) for x in generate_values()]
    print(squared_values)


def q8():
    return lambda lst: sorted(
        [x for x in lst if all(x % i != 0 for i in range(2, int(x ** 0.5) + 1)) and x > 1], reverse=True)


if __name__ == "__main__":
    main()
