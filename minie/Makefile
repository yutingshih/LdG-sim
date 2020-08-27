#!/usr/bin/make

SHELL = /bin/bash

SRCDIR = ./src
INCDIR = ./src
OBJDIR = ./obj
APPDIR = .

SRC = $(wildcard $(SRCDIR)/*.c)
OBJ = $(patsubst $(SRCDIR)/%.c, $(OBJDIR)/%.o, $(SRC))
APP = $(APPDIR)/minie.out

CC = gcc
CFLAGS = -Wall -std=c99 -pedantic -I$(INCDIR)
LDFLAGS = -lm

.PHONY: all build bench clean debug

all: build debug

build:
	@mkdir -p $(OBJDIR) $(APPDIR)

debug: CFLAGS += -g -O0 -DDEBUG
debug: $(APP)
	$(APP)

bench: CFLAGS += -O3
bench: $(APP)

clean:
	-@rm -rvf $(OBJ) $(APP)


$(OBJDIR)/%.o: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(APP): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
