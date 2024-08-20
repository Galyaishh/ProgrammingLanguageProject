def main():
    q1()


def q1():
    fibonacci = lambda n: (lambda f, n: f(f, n))(lambda f, n, a=0, b=1: [] if n == 0 else [a] + f(f, n - 1, b, a + b),
                                                 n)
    print(fibonacci(8))




if __name__ == "__main__":
    main()
