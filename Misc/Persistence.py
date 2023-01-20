# persistence of a number

def func(num, count):
    num_str = str(num)
    if len(num_str) == 1:
        return count
    digits = [int(ele) for ele in num_str]
    result = 1
    for ele in digits:
        result *= ele
    print(result)
    return func(result, count + 1)


def main():
    n = int(input())
    print("Persistence:", func(n, 0))


if __name__ == '__main__':
    main()
