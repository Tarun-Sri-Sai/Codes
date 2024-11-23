def main():
    number = 0
    for i in range(int(1e8)):
        number += i
    print(number, end='\r')


if __name__ == '__main__':
    main()
