/* ising.h*/

#ifndef ISING_H  /* nome della macro usata come inclusion guard, serve 
a evitare duplicazioni*/
#define ISING_H

void initialize_metropolis_lookup(double beta, double *p_lookup);
int energy_difference(int *lattice, int s_r,  int L, int i, int j);
void metropolis_sweep(int *lattice, int L, double beta, double *p_lookup);
void metropolis_sweep_single_update(int *lattice, int L, double beta, double *p_lookup, int i, int j);
double compute_magnetization_volume(int *lattice, int L);
double compute_energy_per_spin(int *lattice, int L);

#endif