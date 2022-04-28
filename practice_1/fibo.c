// fibo.c
// Simple example for profilig workshop
#include <stdio.h>
#include <stdlib.h>

int fibo(int x) {
  if (x == 0) return 0;
  else if (x == 1) return 1;
  return fibo(x - 1) + fibo(x - 2);
}

int main(int argc, char *argv[]) {

  for (size_t i = 0; i < 30; i++) {
    //fibo(i);
    printf("%d\n", fibo(i));
  }
  return 0;
}
