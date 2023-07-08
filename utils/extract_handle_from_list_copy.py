def extract_lines():
    # Read data from a text file
    with open('inputs.txt', 'r', encoding="utf-8") as file:
        input_data = file.read()

    # Split input_data into list of lines
    lines = input_data.split("\n")

    # Filter lines that start with '@'
    at_lines = [line for line in lines if line and line[0] == '@']

    # Write filtered lines to a text file
    with open('output.txt', 'w') as file:
        file.write('\n'.join(at_lines))

def dedupe_txt(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        input_data = file.read()

    lines = input_data.split("\n")

    deduped_lines = list(set(lines))

    with open('output_deduped.txt', 'w') as file:
        file.write('\n'.join(deduped_lines))


if __name__ == '__main__':
    # extract_lines()
    dedupe_txt("./bin/twitter-list-me-and-troj-and-illusts.txt")


