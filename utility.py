import csv


def generate_file(data, file_name):

    with open(file_name + '.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    file.close()
