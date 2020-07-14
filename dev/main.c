#include <stdio.h>
#include <stdlib.h>

float* laplace(float* arr, int size);
float* farray(const int size);
void printa(float* array, const int size, char* prompt);

int main(void)
{
	const int size = 10;
	float arr[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
	float* lap = laplace(arr, size);

	#ifdef DEBUG
	printa(arr, size, "arr:\t");
	printa(lap, size, "lap:\t");
	#endif

	free(lap);
	return 0;
}

float* laplace(float* arr, int size)
{
	float* lap = farray(size);

	for (int i = 0; i < size; i++)
	{
		if (i == 0)
		{
			lap[i] = (arr[size - 3] + arr[1]) / 2 - arr[size - 2];
		}
		else if (i == size - 1)
		{
			lap[i] = (arr[i - 1] + arr[2]) / 2 - arr[1];
		}
		else
		{
			lap[i] = (arr[i - 1] + arr[i + 1]) / 2 - arr[i];
		}
	}
	return lap;
}

float* farray(int size)
{
	float* array = (float*)malloc(size * sizeof(float));
	return array;
}

void printa(float* array, const int size, char* prompt)
{
	printf("%s%f", prompt, *array);
	for (int i = 1; i < size; i++) {
		printf(", %f", array[i]);
	}
	printf("\n");
}
