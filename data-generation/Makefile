# ========== CONFIGURAZIONE ==========

CC = gcc # compilatore
CFLAGS = -Wall -O2 -Iinclude # dice a gcc dove trovare gli header
LDLIBS = -lm # serve per linkare la libreria matematica libm

SRC = src/utils.c src/ising.c src/geometry.c src/random.c src/pcg32min.c # Lista dei sorgenti comuni a entrambi i programmi

# ========== TARGETS ==========

.PHONY: all clean run-main run-tau_exp_main help

all: main tau_exp_main # compila entrambi

# compila e produce gli eseguibili
main: main.c $(SRC)
	$(CC) $(CFLAGS) main.c $(SRC) $(LDLIBS) -o main

tau_exp_main: tau_exp_main.c $(SRC)
	$(CC) $(CFLAGS) tau_exp_main.c $(SRC) $(LDLIBS) -o tau_exp_main

# Esecuzioni rapide
run-main: main
ifndef L
	$(error Devi specificare L: usa 'make run-main L=60')
endif
	./main $(L)

run-tau_exp_main: tau_exp_main
ifndef L
	$(error Devi specificare L: usa 'make run-tau_exp_main L=60')
endif
	./tau_exp_main $(L)

# Pulizia: rimuove gli eseguibili, file oggetto,...
clean:
	rm -f main tau_exp_main *.o *~ log_*.txt log_*.err


# ========== AIUTO ==========

help:
	@echo ""
	@echo "📦 Comandi disponibili:"
	@echo ""
	@echo "  make                - Mostra questo messaggio"
	@echo "  make all            - Compila main e tau_exp_main"
	@echo "  make main           - Compila solo main.c"
	@echo "  make tau_exp_main   - Compila solo tau_exp_main.c"
	@echo "  make run-main       - Mostra come lanciare ./main <L>"
	@echo "  make run-tau_exp_main    - Mostra come lanciare ./tau_exp_main <L>"
	@echo "  make clean          - Rimuove eseguibili, file oggetto e log"
	@echo ""

.DEFAULT_GOAL := help



# make main compila main.c
# make run-main compila ed esegue main.c
# make clean
# make help o make
# make all (compila tutto)
# make make run-cluster-selectable esegue le simulazioni per i vari L su processori diversi per il programma main.c o tau_exp_main.c