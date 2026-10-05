def to_ids(file_lines, line_id_map):

    line_ids = []

    for current_line in file_lines:
        current_line_id = line_id_map.get(current_line)
        if current_line_id is None:
            current_line_id = len(line_id_map)
            line_id_map[current_line] = current_line_id
        line_ids.append(current_line_id)
        
    return line_ids
