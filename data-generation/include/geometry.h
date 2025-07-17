/* geometry.h*/

#ifndef GEOMETRY_H  /* nome della macro usata come inclusion guard, serve 
a evitare duplicazioni*/
#define GEOMETRY_H

int *create_lattice(int L);
void initialize_lattice(int L, int *lattice);
void free_lattice(int **lattice);

#endif