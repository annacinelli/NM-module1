#ifndef UTILS_H
#define UTILS_H


/* struttura Param per contenere una coppia di L, beta */
typedef struct {
    int L;
    double beta;
} Param;

Param *read_param_combinations(const char *filename, int *num_params);

void create_directory_if_needed(const char *path);
void generate_unique_filename(char *folder, char *base_name, char *out_path, int max_len);

#endif
