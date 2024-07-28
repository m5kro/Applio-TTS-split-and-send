import os
import re

# Set chunk size to 15000 characters to prevent memory overload
def split_and_clean_text_file(input_file, chunk_size=15000):
    with open(input_file, 'r') as file:
        text = file.read()

    output_dir = 'chunks'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    start = 0
    chunk_number = 1
    while start < len(text):
        end = start + chunk_size

        # Ensure we end at the end of a sentence
        if end < len(text):
            end = text.rfind('.', start, end) + 1

        # Replace newlines with spaces and remove extra spaces
        chunk_text = text[start:end].replace('\n', ' ')
        chunk_text = re.sub(r' {2,}', ' ', chunk_text)

        with open(os.path.join(output_dir, f'chunk_{chunk_number}.txt'), 'w') as file:
            file.write(chunk_text)

        start = end
        chunk_number += 1

    print(f"Split the text into {chunk_number - 1} chunks in the '{output_dir}' directory.")

input_file = input("Please provide the path to the text file: ")
split_and_clean_text_file(input_file)
