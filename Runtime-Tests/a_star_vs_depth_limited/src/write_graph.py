def get_info(line):
    if line == "{}":
        return "None"

    result = ""
    trimmed_line = line[1:-1]
    vertex_pairs = trimmed_line.split(", ")

    for vertex_pair in vertex_pairs:
        tokens = vertex_pair.split(": ")
        result += str(tokens[0] + ',' + tokens[1].strip() + ' ')

    return result[:-1]


def main():
    with open("../graphs/test.txt", "w") as fwrite:
        n_vertices = int(input("Enter no of vertices: "))
        fwrite.write(str(n_vertices) + "\n")
        fwrite.write(str(2) + "\n")

        for i in range(n_vertices):
            line = input(f"Enter line {i + 1}: ")
            line_trimmed = line[3::]
            fwrite.write(get_info(line_trimmed) + "\n")

        fwrite.write(input("Enter start: ") + "\n")
        fwrite.write(input("Enter end: ") + "\n")
        fwrite.write(str(int(input("Enter depth: "))) + "\n")
        fwrite.write(str(1) + "\n")


if __name__ == "__main__":
    main()
