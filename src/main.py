import sys

import line_identifier
import file_reader
import edit_distance
import diff_formatter


def main():

    command_arguments = sys.argv[1:]

    if len(command_arguments) != 3 or command_arguments[0] not in ("lines", "highlight"):
        print("usage: main.py lines|highlight A_PATH B_PATH", file=sys.stderr)
        sys.exit(2)

    requested_mode, original_file_path, updated_file_path = command_arguments

    try:
        original_lines = file_reader.read_lines(original_file_path)
        updated_lines = file_reader.read_lines(updated_file_path)
        
    except OSError as read_error:
        print(f"error: cannot read file: {read_error}", file=sys.stderr)
        sys.exit(2)

    line_id_map = {}
    original_line_ids = line_identifier.to_ids(original_lines, line_id_map)
    updated_line_ids = line_identifier.to_ids(updated_lines, line_id_map)

    edit_operations = edit_distance.diff(original_line_ids, updated_line_ids)

    diff_formatter.print_diff(edit_operations, original_lines, updated_lines, requested_mode == "highlight")


if __name__ == "__main__":
    main()
