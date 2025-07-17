# Compilatore e flags
CC = gcc
CFLAGS = -Wall -O2 -Iinclude

# Cartelle
SRC_DIR = src
BUILD_DIR = build
BIN_DIR = bin

# File sorgente
SRCS = $(wildcard $(SRC_DIR)/*.c)

# File oggetto corrispondenti in build/
OBJS = $(patsubst $(SRC_DIR)/%.c,$(BUILD_DIR)/%.o,$(SRCS))

# Nome eseguibile
TARGET = ising

# Regola di default
all: $(TARGET)

# Regola per creare l'eseguibile
$(TARGET): $(OBJS)
	@mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) $(OBJS) -o $(BIN_DIR)/$(TARGET)
	@echo "Build complete: $(BIN_DIR)/$(TARGET)"

# Regola per compilare i .c in .o salvando in build/
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# Test geometry, ising e random
test_geometry: build/test_geometry.o build/geometry.o
	$(CC) $(CFLAGS) $^ -o bin/test_geometry

build/test_geometry.o: test/test_geometry.c
	@mkdir -p build
	$(CC) $(CFLAGS) -c $< -o $@

test_ising: build/test_ising.o build/ising.o build/geometry.o build/random.o
	$(CC) $(CFLAGS) $^ -o bin/test_ising

build/test_ising.o: test/test_ising.c
	@mkdir -p build
	$(CC) $(CFLAGS) -c $< -o $@

test_random: build/test_random.o build/random.o
	$(CC) $(CFLAGS) $^ -o bin/test_random

build/test_random.o: test/test_random.c
	@mkdir -p build
	$(CC) $(CFLAGS) -c $< -o $@

# Pulizia, make clean, per es. prima di un commit, per non includere .o ed eseguibili
clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)/$(TARGET)

# Pulizia completa
cleanall:
	rm -rf $(BUILD_DIR) $(BIN_DIR) $(TARGET)

.PHONY: all clean cleanall
