import time
import tracemalloc
from numba import njit

# Função recursiva
def escada_recursiva(n):
    if n == 0:
        return 1
    if n < 0:
        return 0
    return escada_recursiva(n-1) + escada_recursiva(n-2)

# Programação dinâmica
def escada_pd(n):
    if n == 0:
        return 1
    dp = [0] * (n+1)
    dp[0] = 1
    dp[1] = 1
    for i in range(2, n+1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# PD + Numba
@njit
def escada_pd_numba(n):
    if n == 0:
        return 1
    dp = [0] * (n+1)
    dp[0] = 1
    dp[1] = 1
    for i in range(2, n+1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# PD + Numba + Paralelo
@njit(parallel=True)
def escada_pd_numba_paralelo(n):
    if n == 0:
        return 1
    dp = [0] * (n+1)
    dp[0] = 1
    dp[1] = 1
    for i in range(2, n+1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

def medir_media(func, n, repeticoes=10):
    tempos = []
    mems = []
    resultado_final = None
   
    for _ in range(repeticoes):
        tracemalloc.start()
        inicio = time.time()
        resultado = func(n)
        tempo = time.time() - inicio
        memoria = tracemalloc.get_traced_memory()[1] / 1024
        tracemalloc.stop()
       
        tempos.append(tempo)
        mems.append(memoria)
        resultado_final = resultado  
   
    tempo_medio = sum(tempos) / repeticoes
    mem_medio = sum(mems) / repeticoes
   
    print(f"{func.__name__}: resultado = {resultado_final}, "
          f"tempo médio = {tempo_medio:.6f}s, "
          f"memória média = {mem_medio:.2f}KB")

escada_pd_numba(1)
escada_pd_numba_paralelo(1)

n = 30

print("\nRecursivo:")
medir_media(escada_recursiva, n)

print("\nPD:")
medir_media(escada_pd, n)

print("\nPD com Numba:")
medir_media(escada_pd_numba, n)

print("\nPD com Numba e Paralelo:")
medir_media(escada_pd_numba_paralelo, n)