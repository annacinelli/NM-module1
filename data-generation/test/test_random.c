// funzioni di test per le funzioni in random.c

#include <math.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>
#include "random.h"


/* verificare che i double generati siano nell'intervallo corretto [0,1) */
void test_random_generator_doublenorm_1open() {
    int i;
    double r;
    random_generator_init(42, 54);

    for (i = 0; i < 100000; i++) {
        r = random_generator_doublenorm_1open();
        // Deve essere >= 0 e < 1
        if (!(r >= 0.0 && r < 1.0)) {
            printf("FAILED: random_generator_doublenorm_1open out of range: %f\n", r);
            exit(1);
        }
    }
    printf("PASSED: random_generator_doublenorm_1open\n");
}

/* verificare che i double generati siano nell'intervallo corretto (0,1) */
void test_random_generator_doublenorm_open() {
    int i;
    double r;
    random_generator_init(42, 54);

    for (i = 0; i < 100000; i++) {
        r = random_generator_doublenorm_open();
        // Deve essere > 0 e < 1
        if (!(r > 0.0 && r < 1.0)) {
            printf("FAILED: random_generator_doublenorm_open out of range: %f\n", r);
            exit(1);
        }
    }
    printf("PASSED: random_generator_doublenorm_open\n");
}

/* verificare che gli interi siano in [0, RAND_MAX] */
void test_random_generator_int() {
    int i, r;
    random_generator_init(42, 54);

    for (i = 0; i < 100000; i++) {
        r = random_generator_int();
        // Deve essere >= 0 e <= RAND_MAX
        if (!(r >= 0 && r <= RAND_MAX)) {
            printf("FAILED: random_generator_int out of range: %d\n", r);
            exit(1);
        }
    }
    printf("PASSED: random_generator_int\n");
}

