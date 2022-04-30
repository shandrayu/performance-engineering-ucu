# Homework 1. Profiling and program analysis

## Create program

Requirements:

- Calculates Fibonacchi numbers (recursion, non-optimized)
- Sleeps for 5 seconds, then prints for how long it was sleeping
- Write to file ineffectively for 3 minutes
- Download something for 5-7 min


## Recommended tools

- gcc - компілятор
- ltrace -  виклики бібліотек
- strace - системні виклики
- ldd  - список бібліотек
- netstat - моніторинг мережі
- iostat - моніторинг диску
- perf - профілювання бінарних файлів
- gprof  - профілювання бінарних файлів
- gprof2dot ./profile | dot -Tsvg -o output.svg - візуалізація результатів gprof
- valgrind --tool=callgrind - профілювання бінарних файлів
- kcachegrind  - візуалізація
