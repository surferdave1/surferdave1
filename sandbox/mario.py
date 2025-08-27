# ask for pyramid height


def main():
    while True:
        a = get_int("Height: ")
        if a < 9 and a > 0:
            break
    # print pyramid right justified
    spaces = a - 1
    hashes = 1
    while (spaces > -1):
        print_space(spaces)
        print_row(hashes)
        spaces = spaces - 1
        hashes = hashes + 1

    # area to place functions
    # create a function that prints a row of bricks


def print_row(a):
    i = 0
    while (i < a):
        print("#", end="")
        i += 1
    print()


def print_space(b):
    i = 0
    while (i < b):
        print(" ", end="")
        i += 1

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass

# main program
main()