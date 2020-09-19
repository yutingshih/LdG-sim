#!/usr/bin/make

SHELL = /bin/bash

SRCDIR = .
INCDIR = .
OBJDIR = .
APPDIR = .

SRC = $(wildcard $(SRCDIR)/*.c)
OBJ = $(patsubst $(SRCDIR)/%.c, $(OBJDIR)/%.o, $(SRC))
APP = data.out lap.out

CC = gcc
CFLAGS = -Wall -std=c99 -pedantic -I$(INCDIR)
LDFLAGS = -lm

.PHONY: all build clean

all: build data lap

build:
	@if [[ ! -d $(OBJDIR) ]]; then mkdir -p $(OBJDIR); fi
	@if [[ ! -d $(APPDIR) ]]; then mkdir -p $(APPDIR); fi

clean:
	-@rm -rvf $(OBJ) $(APP)

data.out: data.c
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

lap.out: lap.c ../src/matrix.c
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
