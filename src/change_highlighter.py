import edit_distance


def ranges(original_line, updated_line):

    original_text = original_line.decode("utf-8")
    updated_text = updated_line.decode("utf-8")

    character_operations = edit_distance.diff(original_text, updated_text)

    original_ranges, updated_ranges = [], []
    original_position = updated_position = 0
    original_range_start = updated_range_start = -1

    for character_operation in character_operations:
        if character_operation == edit_distance.KEEP:
            if original_range_start >= 0:
                original_ranges.append(f"{original_range_start}-{original_position}")
                original_range_start = -1

            if updated_range_start >= 0:
                updated_ranges.append(f"{updated_range_start}-{updated_position}")
                updated_range_start = -1

            original_position += 1
            updated_position += 1

        elif character_operation == edit_distance.DELETE:
            if original_range_start < 0:
                original_range_start = original_position
            original_position += 1

        else:
            if updated_range_start < 0:
                updated_range_start = updated_position
            updated_position += 1

    if original_range_start >= 0:
        original_ranges.append(f"{original_range_start}-{original_position}")

    if updated_range_start >= 0:
        updated_ranges.append(f"{updated_range_start}-{updated_position}")

    original_range_text = ",".join(original_ranges) if original_ranges else "."
    updated_range_text = ",".join(updated_ranges) if updated_ranges else "."
    
    return f"{original_range_text} | {updated_range_text}"
