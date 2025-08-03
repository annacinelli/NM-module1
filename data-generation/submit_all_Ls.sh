#!/bin/bash
#SBATCH --job-name=ising_L
#SBATCH --output=log_L_%A_%a.out
#SBATCH --error=log_L_%A_%a.err
#SBATCH --array=0-7
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=02:00:00
#SBATCH --mem=2G

# Lista dei valori di L
L_list=(20 40 60 80 100 120 140 160)

# Seleziona L corrispondente a questo task
L=${L_list[$SLURM_ARRAY_TASK_ID]}

# Usa il nome dell'eseguibile passato da sbatch come variabile
EXEC=${EXECUTABLE:-main}  # di default usa "main"

echo "Eseguo ./${EXEC} ${L} su task $SLURM_ARRAY_TASK_ID (job ID $SLURM_JOB_ID)"

# Compilazione (opzionale)
make $${EXEC}

# Esegui
./$${EXEC} ${L}


# make run-cluster-selectable EXECUTABLE=main
# make run-cluster-selectable EXECUTABLE=tau_exp_main

