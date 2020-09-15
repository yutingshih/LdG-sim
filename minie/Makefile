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

.PHONY: all build clean debug release

all: build debug

build:
	@if [[ ! -d $(OBJDIR) ]]; then mkdir -p $(OBJDIR); fi
	@if [[ ! -d $(APPDIR) ]]; then mkdir -p $(APPDIR); fi

debug: CFLAGS += -g -O0 -DDEBUG
debug: $(APP)

release: CFLAGS += -O3 -DNDEBUG
release: $(APP)

clean:
	-@rm -rvf $(OBJ) $(APP)

$(OBJDIR)/%.o: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(APP): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
