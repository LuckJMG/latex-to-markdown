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

file_name = input("File name: ")
input_file = open(file_name + ".tex", "r")
output_file = open(file_name + ".md", "w")

token_stack = []
text_stack = [""]

for line in input_file:
    index = 0
    while index < len(line):
        char = line[index]

        # Enter new parenthesis
        if char == "\\":
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
        if char == "}":
            token = token_stack.pop()
            text = text_stack.pop()

            text_stack[len(text_stack) - 1] += (
                TOKENS[token][0] + text + TOKENS[token][1]
            )  #! Only wrapping
            index += 1
            continue

        text_stack[len(text_stack) - 1] += char
        index += 1

output_file.write(text_stack[0])

input_file.close()
output_file.close()
print("Convertion Completed")
