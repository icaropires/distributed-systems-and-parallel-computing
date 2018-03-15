#ifndef UTILS_H_
#define UTILS_H_

#include <stdio.h>

typedef struct pdu {
    int a;
    int b;
    char operator;
    int result;
} Package;

Package get_filled_package();

int calculate(Package package);

int add(int a, int b);

int sub(int a, int b);

int multiply(int a, int b);

int divide(int a, int b);

#endif  // UTILS_H_
