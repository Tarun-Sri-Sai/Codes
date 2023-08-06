CC=g++
CPPFLAGS=-Wall -Wextra -Wpedantic -Werror
RM=del /F /Q

all: bin/main.exe

bin/main.exe: obj/main.o obj/sorter.o
	@$(CC) $(CPPFLAGS) $^ -o $@

obj/sorter.o: src/sorter.cpp
	@$(CC) $(CPPFLAGS) -c $^ -o $@

obj/main.o: main.cpp
	@$(CC) $(CPPFLAGS) -c $^ -o $@

run:
	@./bin/main.exe

clean:
	@$(RM) obj\*