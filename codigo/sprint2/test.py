def main():
    for x in range(0, 100000000):
        if x * x != pow(x, 2):
            print(x)
main()