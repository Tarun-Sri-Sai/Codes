CC=gcc
CPPFLAGS=-Wall -Wextra -Wpedantic -Werror


all: bin/linked_list_test.exe

bin/linked_list_test.exe: obj/main.o obj/linked_list.o obj/list_node.o
	${CC} $^ -o $@

obj/%.o: src/%.c
	${CC} ${CPPFLAGS} -c $^ -o $@

obj/%.o: test/%.c
	${CC} ${CPPFLAGS} -c $^ -o $@

clean:
	rm obj/*.o bin/*.exe
