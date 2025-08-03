#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdbool.h>
#include "utils.h"


int main(void) {
    const char *results_dir = "results";
    char base_name[100];
    char full_path[200];
    int L_test = 160;
    double beta_test = 0.5;
    int num_beta = 10;

    // Test 1: creare directory se non esiste
    create_directory_if_needed(results_dir);
    printf("Directory '%s' verificata o creata.\n", results_dir);

    // Test 2: generare file unico per la prima combinazione
    snprintf(base_name, sizeof(base_name), "L%d_beta%.6f", L_test, beta_test);
    generate_unique_filename((char *)results_dir, base_name, full_path, sizeof(full_path));
    printf("Nome file unico generato: %s\n", full_path);

    // Test 3: testare generate_beta_range

    printf("\n--- Test generazione range beta per L = %d ---\n", L_test);
    double *betas = generate_beta_range(L_test, &num_beta);

    if (betas != NULL) {
        for (int i = 0; i < num_beta; i++) {
            printf("beta[%2d] = %.8f\n", i, betas[i]);
        }
        free(betas); // libera memoria
    } else {
        fprintf(stderr, "Errore: generazione betas fallita\n");
    }

    return 0;
}