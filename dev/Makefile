#!/usr/bin/make

SHELL = /bin/bash

SRCDIR = .
INCDIR = .
OBJDIR = .
APPDIR = .

SRC = $(wildcard $(SRCDIR)/*.c)
OBJ = $(patsubst $(SRCDIR)/%.c, $(OBJDIR)/%.o, $(SRC))
APP = lap.exe

CC = gcc
CFLAGS = -Wall -std=c99 -I$(INCDIR)

.PHONY: all bench clean debug

all: bench

debug: CFLAGS += -g -O0 -DDEBUG
debug: $(APP)

bench: CFLAGS += -O3
bench: $(APP)

$(OBJDIR)/%.o: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(APP): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	-rm -rvf $(OBJDIR)/*.o $(APPDIR)/*.exe
