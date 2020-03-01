CC=clang++
CFLAGS=
LINK=-ldl -lglfw
DEPS = hellomake.h

%.o: %.cpp $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

clean:
	rm *.o

hellotriangle: glad.o hellotriangle.o
	$(CC) -o hellotriangle hellotriangle.o glad.o $(LINK)


hellotexture: glad.o hellotexture.o
	$(CC) -o hellotexture hellotexture.o glad.o $(LINK)


hellocamera: glad.o hellocamera.o
	$(CC) -o hellocamera hellocamera.o glad.o $(LINK)
