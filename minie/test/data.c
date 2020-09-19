#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUMBER_OF_MATRICES 12393
#define NUMBER_OF_ELEMENTS 9

int main(int argc, const char* argv[])
{
	srand(time(NULL));
	for (int i = 0; i < NUMBER_OF_MATRICES * NUMBER_OF_ELEMENTS; i++)
		printf("%lf ", (double)rand());
	printf("\n");
	return 0;
}
