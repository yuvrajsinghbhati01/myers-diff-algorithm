KEEP = 0
DELETE = 1
INSERT = 2


def diff(source_sequence, target_sequence):

    source_length, target_length = len(source_sequence), len(target_sequence)

    common_prefix_length = 0
    while common_prefix_length < source_length and common_prefix_length < target_length and source_sequence[common_prefix_length] == target_sequence[common_prefix_length]:
        common_prefix_length += 1
    common_suffix_length = 0

    while common_suffix_length < source_length - common_prefix_length and common_suffix_length < target_length - common_prefix_length and source_sequence[source_length - 1 - common_suffix_length] == target_sequence[target_length - 1 - common_suffix_length]:
        common_suffix_length += 1

    middle_edit_script = _search(source_sequence[common_prefix_length:source_length - common_suffix_length], target_sequence[common_prefix_length:target_length - common_suffix_length])
    return [KEEP] * common_prefix_length + middle_edit_script + [KEEP] * common_suffix_length


def _search(source_sequence, target_sequence):

    source_length, target_length = len(source_sequence), len(target_sequence)
    maximum_edits = source_length + target_length
    furthest_x_by_diagonal = [0] * (2 * maximum_edits + 3)
    diagonal_storage_size = len(furthest_x_by_diagonal)
    search_trace = []
    minimum_edit_count = 0

    reached_target = False
    for edit_count in range(maximum_edits + 1):
        for diagonal in range(-edit_count, edit_count + 1, 2):
            if diagonal == -edit_count or (diagonal != edit_count and furthest_x_by_diagonal[diagonal - 1] < furthest_x_by_diagonal[diagonal + 1]):
                source_position = furthest_x_by_diagonal[diagonal + 1]

            else:
                source_position = furthest_x_by_diagonal[diagonal - 1] + 1
            target_position = source_position - diagonal

            while source_position < source_length and target_position < target_length and source_sequence[source_position] == target_sequence[target_position]:
                source_position += 1
                target_position += 1
            furthest_x_by_diagonal[diagonal] = source_position

            if source_position >= source_length and target_position >= target_length:
                minimum_edit_count = edit_count
                reached_target = True
                break

        search_trace.append(furthest_x_by_diagonal[:edit_count + 1] + furthest_x_by_diagonal[diagonal_storage_size - edit_count:] if edit_count > 0 else furthest_x_by_diagonal[:1])
        
        if reached_target:
            break

    edit_operations = []
    source_position, target_position = source_length, target_length

    for edit_count in range(minimum_edit_count, 0, -1):
        previous_trace = search_trace[edit_count - 1]
        diagonal = source_position - target_position

        if diagonal == -edit_count or (diagonal != edit_count and previous_trace[diagonal - 1] < previous_trace[diagonal + 1]):
            previous_diagonal = diagonal + 1

        else:
            previous_diagonal = diagonal - 1
        previous_source_position = previous_trace[previous_diagonal]
        previous_target_position = previous_source_position - previous_diagonal

        while source_position > previous_source_position and target_position > previous_target_position:
            edit_operations.append(KEEP)
            source_position -= 1
            target_position -= 1
        edit_operations.append(INSERT if previous_diagonal == diagonal + 1 else DELETE)
        source_position, target_position = previous_source_position, previous_target_position
        
    while source_position > 0 and target_position > 0:
        edit_operations.append(KEEP)
        source_position -= 1
        target_position -= 1

    edit_operations.reverse()
    return edit_operations
