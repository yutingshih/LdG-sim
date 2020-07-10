#!/bin/bash

function lapC()
{
	APP=$2
	TIMES=${1:-1}
	for (( i = 0; i < $TIMES; i++ )); do
		$APP
	done
}

function lapP()
{
	APP=$2
	TIMES=${1:-1}
	for (( i = 0; i < $TIMES; i++ )); do
		$APP
	done
}

function bench()
{
	TIMES=${1:-10}
	Cfile=./lap.exe
	Pfile=./lap.py

	printf "Run $Pfile $TIMES times"
	time lapP $TIMES $Pfile

	printf "\nRun $Cfile $TIMES times"
	time lapC $TIMES $Cfile
}

bench $1
