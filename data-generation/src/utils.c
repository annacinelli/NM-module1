#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <stdbool.h>
#include <math.h>
#include "utils.h"

#define BETA_C 0.4406867935
#define NU     1.0
#define WIDTH_FACTOR 1.0     // fattore moltiplicativo per la finestra: serve a controllare quanto largo è il range di beta simulato per ogni L
#define NUM_BETA 40          // numero di beta per ogni L


/* controlla se esite già la cartella 'results' per esempio, altrimenti la crea */
void create_directory_if_needed(const char *path) {
    struct stat st = {0}; /* crea una struttura stat (<sys/stat.h>), serve per controllare informazioni sulla cartella */

    if (stat(path, &st) == -1) {  /* stat() controlla se la cartella esiste, se -1 (non esiste o c'è un errore, 0 se esiste), tenta di crearla;
        la funzione stat() riempie il contenuto della struttura st con informazioni sulla directory path */
        if (mkdir(path, 0755) != 0) {
            perror("mkdir"); /* stampa un messaggio di errore relativo all’ultima operazione fallita */
            exit(EXIT_FAILURE);
        }
    }
}


/* genera un nome di file che non esiste ancora, nella cartella folder, con prefisso base_name, seguito da una versione numerata */
void generate_unique_filename(char *folder, char *base_name, char *out_path, int max_len) {
    int version = 1;

    snprintf(out_path, max_len, "%s/%s_v%d.txt", folder, base_name, version); /* genera il primo nome candidato;
    'string formatted print with limit': scrive una stringa formattata (come printf), ma la scrive in un buffer,
    cioè in una variabile char[], senza superare una certa lunghezza massima */
    FILE *fp = fopen(out_path, "r");

    while (fp != NULL) {
        fclose(fp);
        version++;
        snprintf(out_path, max_len, "%s/%s_v%d.txt", folder, base_name, version);
        fp = fopen(out_path, "r");
    }
}


/* genera un array di beta centrati su BETA_C e distribuiti in modo uniforme in: [BETA_C - c * L^{-1/nu}, BETA_C + c * L^{-1/nu}];
ritorna il puntatore all'array; c = 1.0 viene dai collapse plots noti per Ising 2D  */
double* generate_beta_range(int L, int *num_beta) {
    double delta = WIDTH_FACTOR * pow(L, -1.0 / NU);
    double beta_min = BETA_C - delta;
    double beta_max = BETA_C + delta;

    *num_beta = NUM_BETA;
    double *betas = malloc(NUM_BETA * sizeof(double));
    if (!betas) {
        fprintf(stderr, "Errore: allocazione array beta fallita\n");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < NUM_BETA; i++) {
        betas[i] = beta_min + i * (beta_max - beta_min) / (NUM_BETA - 1);
    }

    return betas;
}
/* poi deallocare */


/* dato L, filename è data-analysis/tau_exp_results.txt, restitisce il tau_exp stimato */
unsigned long long read_tau_exp_from_file(int L, const char *filename) {
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        fprintf(stderr, "Errore: impossibile aprire %s\n", filename);
        exit(EXIT_FAILURE);
    }

    char line[160];
    int file_L; /* per leggere temporaneamente il valore di L dalla riga */
    unsigned long long tau;

    while (fgets(line, sizeof(line), fp)) {
        if (line[0] == '#') continue; /* salta le righe che iniziano con # (commenti o intestazioni) */
        /* se trova due valori prosegue */
        if (sscanf(line, "%d\t%llu", &file_L, &tau) == 2) {
            if (file_L == L) {
                fclose(fp);
                return tau;
            }
        }
    }

    fclose(fp);
    fprintf(stderr, "Errore: valore di L = %d non trovato in %s\n", L, filename);
    exit(EXIT_FAILURE);
}



/* caso colonne, makefile, tipi, riguardare utils.py e macro, valori T */