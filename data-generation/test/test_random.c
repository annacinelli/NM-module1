#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "random.h"
#include "pcg32min.h"


/* tests */
int main(void) {
    const int N = 1000000;  /* numero di test */
    double x;
    int r, min_int = RAND_MAX, max_int = 0;

    random_generator_init(42, 54);  /* valori fissi per test riproducibili */

    printf("Testing random_generator_doublenorm_1open (in [0,1))...\n");
    for (int i = 0; i < N; i++) {
        x = random_generator_doublenorm_1open();
        assert(x >= 0.0 && x < 1.0);
    }

    printf("Testing random_generator_doublenorm_open (in (0,1))...\n");
    for (int i = 0; i < N; i++) {
        x = random_generator_doublenorm_open();
        assert(x > 0.0 && x < 1.0);
    }

    printf("Testing random_generator_int (in [0, RAND_MAX])...\n");
    for (int i = 0; i < N; i++) {
        r = random_generator_int();
        assert(r >= 0 && r <= RAND_MAX);
        if (r < min_int) min_int = r;
        if (r > max_int) max_int = r;
    }

    printf("All tests passed.\n");
    printf("Min int observed: %d, Max int observed: %d\n", min_int, max_int);

    return 0;
}