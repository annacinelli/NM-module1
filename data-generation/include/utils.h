#ifndef UTILS_H
#define UTILS_H

void create_directory_if_needed(const char *path);
void generate_unique_filename(char *folder, char *base_name, char *out_path, int max_len);
double* generate_beta_range(int L, int *num_beta);
unsigned long long read_tau_exp_from_file(int L, const char *filename);

#endif
