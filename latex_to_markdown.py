import re

# TOKENS = {
#     "documentclass": "",
#     "usepackage": "",
#     "title": "# ",
#     "author": "author: ",
#     "date": "created date: ",
#     "newtheorem": "",
#     "begindocument": "",
#     "enddocument": "",
#     "maketitle": "",
#     "talbeofcontents": "",
#     "newpage": "---",
#     "section": "## ",
#     "[": "$$",
#     "]": "$$",
# }

TOKENS = {
    "textbf": ("**", "**"),
    "title": ("# ", ""),
    "section": ("## ", ""),
    "subsection": ("### ", ""),
}

REPLACE_TOKENS = {
    "\\maketitle\n": "",
    "\\tableofcontents\n": "",  #! Create a table of contents
    "\\newpage": "---",
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

title = ""
file_name = input("File name: ")
input_file = open(file_name + ".tex", "r")
output_file = open(file_name + ".md", "w")

token_stack = []
text_stack = [""]

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
    for key, value in REPLACE_TOKENS.items():
        if key in line:
            line = line.replace(key, value)

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
                token += char
                index += 1
                char = line[index]

            token_stack.append(token)
            text_stack.append("")
            index += 1
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
print("Convertion Completed")
