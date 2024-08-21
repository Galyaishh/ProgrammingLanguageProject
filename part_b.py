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
    return list(map(
        lambda sublist: reduce(
            lambda cum_sum, x: cum_sum + x,  # Sum of squares
            map(
                lambda y: y**2,  # Square the even numbers
                filter(
                    lambda z: z % 2 == 0,  # Filter even numbers
                    sublist
                )
            ),
            0  # Initial cumulative sum is 0
        ),
        lst  # Apply to each sublist
    ))

def q4():

    def accumulate(binary_op):
        def inner(sequence, initial=None):
            if not sequence:
                return initial
            if initial is None:
                initial = sequence[0]
                sequence = sequence[1:]
            for x in sequence:
                initial = binary_op(initial, x)
            return initial

        return inner

    factorial = accumulate(lambda x, y: x * y)
    print(factorial([1, 2, 3, 4, 5]))  # Output: 120

    exponentiation = accumulate(lambda x, y: x ** y)
    print(exponentiation([2, 3, 4]))



if __name__ == "__main__":
    main()
