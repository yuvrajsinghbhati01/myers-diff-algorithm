import sys

import change_highlighter
import edit_distance


def print_diff(edit_operations, original_lines, updated_lines, show_highlights):

    output_parts = []
    original_index = updated_index = 0
    operation_index = 0
    operation_count = len(edit_operations)

    while operation_index < operation_count:
        if edit_operations[operation_index] == edit_distance.KEEP:
            output_parts.append(b" " + original_lines[original_index] + b"\n")
            original_index += 1
            updated_index += 1
            operation_index += 1
            continue

        deleted_lines, inserted_lines = [], []

        while operation_index < operation_count and edit_operations[operation_index] != edit_distance.KEEP:
            if edit_operations[operation_index] == edit_distance.DELETE:
                deleted_lines.append(original_lines[original_index])
                original_index += 1

            else:
                inserted_lines.append(updated_lines[updated_index])
                updated_index += 1
            operation_index += 1

        for current_line in deleted_lines:
            output_parts.append(b"-" + current_line + b"\n")
        paired_line_count = min(len(deleted_lines), len(inserted_lines))

        for inserted_line_index, current_line in enumerate(inserted_lines):
            output_parts.append(b"+" + current_line + b"\n")
            if show_highlights and inserted_line_index < paired_line_count:
                highlight_text = "? " + change_highlighter.ranges(deleted_lines[inserted_line_index], current_line) + "\n"
                output_parts.append(highlight_text.encode("ascii"))
                
    sys.stdout.buffer.write(b"".join(output_parts))
    sys.stdout.buffer.flush()
