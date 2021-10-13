

def write_columns(ws, columns, font_style, row_num):
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        col = ws.col(col_num)
        col.width = 256*(len(columns[col_num])+5)
