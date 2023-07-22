TOKENS = {
    "textbf": ("**", "**"),
    "title": ("# ", ""),
    "section": ("## ", ""),
    "subsection": ("### ", ""),
    "includegraphics": ("![[", "]]"),
    "paragraph": ("", ""),
}

REPLACE_TOKENS = {
    "\\maketitle\n": "",
    "\\tableofcontents\n": "",  #! Create a table of contents
    "\\newpage": "---\n",
    "\\[": "$$",
    "\\]": "$$",
}

METADATA = {
    "documentclass": "type: ",
    "author": "author: ",
    "date": "created date: ",
    "usepackage": "packages: ",
    "title": "# ",
}

math_mode = False
multiline_math_mode = False
special_mode = []
enumerate_count = []

title = ""
file_name = input("File name: ")
input_file = open(file_name + ".tex", "r")
output_file = open(file_name + ".md", "w")

token_stack = []
text_stack = [""]

# METADATA
output_file.write("---\n")

for line in input_file:
    index = 0

    while index < len(line):
        char = line[index]

        if char == "\\":
            index += 1
            token = ""

            # Get token
            char = line[index]
            while char != "{":
                token += char
                index += 1
                char = line[index]

            if token not in METADATA.keys():
                break

            index += 1
            info = ""

            # Get metadata
            char = line[index]
            while char != "}":
                info += char
                index += 1
                char = line[index]

            if token == "title":
                title = info
                continue

            output_file.write(METADATA[token] + info + "\n")

        index += 1

    if "\\begin{document}" in line:
        break

output_file.write("---\n\n")
output_file.write(METADATA["title"] + title)

for line in input_file:
    if line == "\\end{document}" or line == "\\end{document}\n":
        break

    for key, value in REPLACE_TOKENS.items():
        if key in line:
            line = line.replace(key, value)

    # Handle special modes
    if len(special_mode) != 0:
        match special_mode[len(special_mode) - 1]:
            case "itemize":
                line = line.replace("    \\item", "-")
            case "enumerate":
                enumerate_count[len(enumerate_count) - 1] += 1
                line = line.replace(
                    "\\item", f"{enumerate_count[len(enumerate_count)-1]}."
                )
            case _:
                line = ("> " * len(special_mode)) + line

    index = 0
    while index < len(line):
        char = line[index]

        # Enter and exit math mode
        if char == "$":
            if line[index + 1] == "$":
                multiline_math_mode = not multiline_math_mode
            else:
                math_mode = not math_mode

        # Enter new parenthesis
        if char == "\\" and not math_mode and not multiline_math_mode:
            index += 1
            token = ""

            # Get token
            char = line[index]
            while char != "{":
                if token not in TOKENS.keys():
                    token += char
                index += 1
                char = line[index]

            index += 1

            # Special modes
            if token == "begin":
                mode = ""
                char = line[index]
                while char != "}":
                    mode += char
                    index += 1
                    char = line[index]

                special_mode.append(mode)

                match mode:
                    case "enumerate":
                        enumerate_count.append(0)
                    case "itemize":
                        pass
                    case _:
                        text_stack[len(text_stack) - 1] += (
                            "> " * len(special_mode)
                        ) + mode

                        if line[index + 1] == "[":
                            name = ""
                            index += 2
                            char = line[index]
                            while char != "]":
                                name += char
                                index += 1
                                char = line[index]

                            text_stack[len(text_stack) - 1] += f" - {name}"

                index += 1
                continue

            elif token == "end":
                mode = special_mode.pop()

                if mode == "enumerate":
                    enumerate_count.pop()

                index += len(mode) + 1
                continue

            token_stack.append(token)
            text_stack.append("")
            continue

        # Exit a parenthesis
        if char == "}" and not math_mode and not multiline_math_mode:
            token = token_stack.pop()
            text = text_stack.pop()

            text_stack[len(text_stack) - 1] += (
                TOKENS[token][0] + text + TOKENS[token][1]
            )
            index += 1
            continue

        text_stack[len(text_stack) - 1] += char
        index += 1

output_file.write(text_stack[0])

input_file.close()
output_file.close()
print(f"{file_name}.tex has been converted to {file_name}.md succesfully")
