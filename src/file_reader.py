def read_lines(file_path):

    with open(file_path, "rb") as input_file:
        file_bytes = input_file.read()

    file_lines = file_bytes.split(b"\n")

    if file_lines[-1] == b"":
        file_lines.pop()
        
    return file_lines
