import os
import xml.etree.ElementTree as ET
import csv
import shutil

# Parse the XML file
tree = ET.parse('csv2json.xml')
root = tree.getroot()

# List to store extracted test cases
test_cases = []
headers = ['Test No.','T_OPTION', 'D_OPTION', 'S_OPTION', 'VALID_INPUT', 'VALID_OUTPUT', 'FIELD_SEPARATOR', 'IS_FILE_EMPTY', 'BOOL_NUM']

for testcase in root.findall('./Testset/Testcase'):
    tc_data = {}
    values = testcase.findall('./Value')
    for header, value_element in zip(headers, values):
        tc_data[header] = value_element.text
    test_cases.append(tc_data)

# Print extracted test cases
for idx, testcase in enumerate(test_cases):
    print(f'Testcase {idx}: {testcase}')

albums = ['SOS', 'Nicole', '"Pure BS"', 'Nurture']
artists = ['SZA', 'NIKI', '"Blake Shelton"', '"Porter Robinson"']
genres = ['R&B', 'Pop', 'Country', 'EDM']
years = [2022, 2022, 2021, 2007]
recs = [True, True, False, True]

folder_name = "AutoTest"
os.makedirs(folder_name, exist_ok=True)

for testcase in test_cases:
    filename = "TestData" + str(testcase['Test No.']) + ".csv"

    if testcase['IS_FILE_EMPTY'] == 'true':
        with open(filename, "w", newline="") as csv_file:
            pass
    else:
        delimiter = ""
        if testcase['T_OPTION'] == 'true':
            delimiter = '\t'
        else:
            if testcase['FIELD_SEPARATOR'] == 'comma':
                delimiter = ","
            elif testcase['FIELD_SEPARATOR'] == 'colon':
                delimiter = ":"
            elif testcase['FIELD_SEPARATOR'] == 'tab':
                delimiter = '\t'
            else:
                delimiter = ","  
        

        with open(filename, 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=delimiter, quoting=csv.QUOTE_NONE, escapechar=' ')
            
            if testcase['BOOL_NUM'] == 'true':
                csv_writer.writerow(["Album", "Artist", "Genre", "Year", "Recommended"])
                for album, artist, genre, year, rec in zip(albums, artists, genres, years, recs):
                    csv_writer.writerow([album, artist, genre, year, rec])

            else:
                csv_writer.writerow(["Album", "Artist", "Genre"])
                for album, artist, genre in zip(albums, artists, genres):
                    csv_writer.writerow([album, artist, genre])
        
    destination = os.path.join(folder_name, filename)
    shutil.move(filename, destination)

print("CSV files have been moved to the folder:", folder_name)