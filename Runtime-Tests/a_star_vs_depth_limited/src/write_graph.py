def get_info(line):
    if line == "{}":
        return "None"
    
    result = ""
    trimmed_line = line[1:-1]
    vertex_pairs = trimmed_line.split(",\\s+")
    
    for vertex_pair in vertex_pairs:
        tokens = vertex_pair.split(":\\s+")
        result += str(tokens[0][1:-1] + ',' + tokens[1] + ' ')

    return result[:-1]


def main():
    with open("../graphs/26nodes.txt", "w") as fwrite:
        n_vertices = int(input())
        fwrite.write(str(n_vertices) + "\n")
        fwrite.write(str(2) + "\n")

        for _ in range(n_vertices):
            line = input()
            line_trimmed = line[3::]
            fwrite.write(get_info(line_trimmed) + "\n")

        fwrite.write(input() + "\n")
        fwrite.write(input() + "\n")
        fwrite.write(str(int(input())) + "\n")
        fwrite.write(str(int(input())) + "\n")


if __name__ == "__main__":
    main()