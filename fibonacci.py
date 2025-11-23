import time
import tracemalloc
from numba import njit


REPETICOES = 10


# Python Recursivo Puro
def fibonacci_recursivo(n):
    if n <= 1:
        return n
    return fibonacci_recursivo(n-1) + fibonacci_recursivo(n-2)


# Python com Programação Dinâmica
def fibonacci_dp(n):
    if n <= 1:
        return n
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib[n]


# Numba
@njit
def fibonacci_numba(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b


def medir_media(func, n):
    tempos = []
    memorias = []


    for _ in range(REPETICOES):
        tracemalloc.start()
        inicio = time.perf_counter()
        func(n)
        fim = time.perf_counter()
        _, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()


        tempos.append(fim - inicio)
        memorias.append(pico / 1024 / 1024)


    print(f"Média de tempo: {sum(tempos) / REPETICOES:.6f} s")
    print(f"Média de pico de memória: {sum(memorias) / REPETICOES:.6f} MB")
    print("-" * 50)




if __name__ == "__main__":
    N = 40


    print("\n--- Fibonacci Recursivo (Python Puro) ---")
    medir_media(fibonacci_recursivo, N)


    print("\n--- Fibonacci com Programação Dinâmica (Python Puro) ---")
    medir_media(fibonacci_dp, N)


    print("\n--- Fibonacci com Numba ---")
    medir_media(fibonacci_numba, N)
