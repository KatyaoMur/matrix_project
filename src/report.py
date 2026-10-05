def format_matrix(matrix):
    lines = [str([round(x, 2) for x in row]) for row in matrix]
    return "\n".join(lines)
