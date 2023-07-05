def read_file(add):
    with open(add, 'r') as file:
        array = [line.strip() for line in file.readlines()]
        return array