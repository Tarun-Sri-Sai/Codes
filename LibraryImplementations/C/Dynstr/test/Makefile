CC=gcc
CPPFLAGS=-Wall -Wextra -Wpedantic -Werror


all: bin/dynstr_test.exe

bin/%.exe: obj/main.o obj/dynstr.o
	${CC} $^ -o $@

obj/%.o: src/%.c
	${CC} ${CPPFLAGS} -c $^ -o $@

obj/%.o: test/%.c
	${CC} ${CPPFLAGS} -c $^ -o $@

clean:
	rm obj/*.o bin/*.exe
