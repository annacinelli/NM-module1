#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdbool.h>
#include "utils.h"

#define MAX_LINE_LEN 200 /* numero massimo di caratteri che si possono leggere da una riga del file */
#define MAX_VALUES 300

/* restituisce un array di Param, cioè di strutture che contengono le coppie di valori letti */
Param *read_param_combinations(const char *filename, int *num_params) {

    FILE *fp = fopen(filename, "r"); /* apre il file txt, se non lo trova dà errore */
    if (fp == NULL) {
        fprintf(stderr, "Error: cannot open file %s\n", filename);
        exit(EXIT_FAILURE);
    }

    char line[MAX_LINE_LEN];
    int L_values[MAX_VALUES];
    double beta_values[MAX_VALUES];
    int L_count = 0, beta_count = 0; /* conteggi per i valori di L, beta */

    fgets(line, MAX_LINE_LEN, fp); // salta intestazione

    while (fgets(line, MAX_LINE_LEN, fp)) {
        int L;
        double beta;
        char *L_str = NULL;
        char *beta_str = NULL;

        // Separazione della riga su base del tab
        L_str = strtok(line, "\t\n");
        beta_str = strtok(NULL, "\t\n");

        // Prova a convertire L se esiste
        if (L_str != NULL && strlen(L_str) > 0) {
            if (sscanf(L_str, "%d", &L) == 1) {
                L_values[L_count++] = L;
            }
        }

        // Prova a convertire beta se esiste
        if (beta_str != NULL && strlen(beta_str) > 0) {
            if (sscanf(beta_str, "%lf", &beta) == 1) {
                beta_values[beta_count++] = beta;
            }
        }
    }

    fclose(fp);

    if (L_count == 0 || beta_count == 0) {
        fprintf(stderr, "Error: at least one L and one beta value required\n");
        exit(EXIT_FAILURE);
    }

    *num_params = L_count * beta_count;
    Param *params = malloc((*num_params) * sizeof(Param));
    if (params == NULL) {
        fprintf(stderr, "Error: memory allocation failed\n");
        exit(EXIT_FAILURE);
    }

    int idx = 0;
    for (int i = 0; i < L_count; i++) {
        for (int j = 0; j < beta_count; j++) {
            params[idx].L = L_values[i];
            params[idx].beta = beta_values[j];
            idx++;
        }
    }

    return params;
}



/* controlla se esite già la cartella 'results', altrimenti la crea;
char *path: una stringa è semplicemente un array di caratteri terminato da '\0' */
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

/* serve a generare un nome di file unico in una certa cartella, genera la nuova versione */
void generate_unique_filename(char *folder, char *base_name, char *out_path, int max_len) {
    int version = 1;

    snprintf(out_path, max_len, "%s/%s_v%d.txt", folder, base_name, version); /* genera il primo nome candidato;
    'string formatted print with limit': scrive una stringa formattata (come printf), ma la scrive in un buffer,
    cioè in una variabile char[], non sullo schermo, senza superare una certa lunghezza massima */
    FILE *fp = fopen(out_path, "r");

    while (fp != NULL) {
        fclose(fp);
        version++;
        snprintf(out_path, max_len, "%s/%s_v%d.txt", folder, base_name, version);
        fp = fopen(out_path, "r");
    }
}
