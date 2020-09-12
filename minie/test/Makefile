#!/usr/bin/make

SHELL = /bin/bash

SRCDIR = .
INCDIR = .
OBJDIR = .
APPDIR = .

SRC = $(wildcard $(SRCDIR)/*.c)
OBJ = $(patsubst $(SRCDIR)/%.c, $(OBJDIR)/%.o, $(SRC))
APP = $(APPDIR)/gen.out

CC = gcc
CFLAGS = -Wall -std=c99 -pedantic -I$(INCDIR)
LDFLAGS = -lm

.PHONY: all build clean

all: build $(APP)

build:
	@if [[ ! -d $(OBJDIR) ]]; then mkdir -p $(OBJDIR); fi
	@if [[ ! -d $(APPDIR) ]]; then mkdir -p $(APPDIR); fi

clean:
	-@rm -rvf $(OBJ) $(APP)

$(OBJDIR)/%.o: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(APP): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
