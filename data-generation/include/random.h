/* random.h*/

#ifndef RANDOM_H  /* nome della macro usata come inclusion guard, serve 
a evitare duplicazioni*/
#define RANDOM_H

void random_generator_init(unsigned long int initstate, unsigned long int initseq);
double random_generator_doublenorm_1open(void);
double random_generator_doublenorm_open(void);
int random_generator_int(void);

#endif