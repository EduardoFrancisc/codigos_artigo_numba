import time
import tracemalloc
import random
from numba import njit, prange


REPETICOES = 10


# Python Puro
def monte_carlo_python(n):
    dentro = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1:
            dentro += 1
    return 4 * dentro / n


# Numba
@njit
def monte_carlo_numba(n):
    dentro = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1:
            dentro += 1
    return 4 * dentro / n


# Numba Paralelo
@njit(parallel=True)
def monte_carlo_numba_parallel(n):
    dentro = 0
    for i in prange(n):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1:
            dentro += 1
    return 4 * dentro / n


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
    N = 5_000_000


    print("\n--- MONTE CARLO: Python Puro ---")
    medir_media(monte_carlo_python, N)


    print("\n--- MONTE CARLO: Numba ---")
    medir_media(monte_carlo_numba, N)


    print("\n--- MONTE CARLO: Numba Paralelo ---")
    medir_media(monte_carlo_numba_parallel, N)
