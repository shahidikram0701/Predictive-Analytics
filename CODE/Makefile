output: client.o prediction.o
	gcc -w client.o prediction.o -o output

client.o: client.c prediction.h
	gcc -c -w client.c

prediction.o: prediction.c prediction.h
	gcc -c -w prediction.c

run:
	./output
