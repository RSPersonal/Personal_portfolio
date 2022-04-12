import csv


def write_portfolio_data_to_csv(file_name: str, headers: list, row_data: list):
    """
    @param file_name:
    @param headers:
    @param row_data:
    @return:
    """
    with open(f"{file_name}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in row_data:
            writer.writerow(row)

    return file


write_portfolio_data_to_csv('test', ['Header 1', 'Header 2', 'Header 3'], [[30, 40, 30], [40, 540, 50]])
