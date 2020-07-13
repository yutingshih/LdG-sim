#!/bin/bash

project=LdG-sim
version=0.3a
name=bench

function run()
{
	program=$1
	times=${2:-1}
	for (( i = 0; i < $times; i++ )); do
		$program
	done
}

function usage()
{
	echo "usage: bench [-h] [-V] [-t TIMES] [-o OUTPUT] [-l] PROGRAMS"
	echo "  -h, --help   	display the help message"
	echo "  -V, --version	show the version number of the LdG-sim project"
	echo "  -t, --times  	specify how many times the benchmark runs, default: 10"
	echo "  -o, --output 	save result to the log file"
}

function bench()
{
	times=10
	output=/dev/null

	while [[ $1 =~ ^- && ! $1 == -- ]]; do
		case $1 in
			-h | --help )
				usage
				;;
			-V | --version )
				echo $project $version $name
				;;
			-t | --times )
				shift; times=$1
				;;
			-o | --output )
				shift; output=$1
				;;
		esac; shift;
	done

	printf "$name $(date +"%Y-%m-%d %H:%M:%S")\n\n" >> $output
	for program in $@; do
		printf "run $program $times times" | tee -a $output
		{ time run $program $times; } 2>&1 | tee -a $output
		echo '' >> $output
	done
}

bench $@