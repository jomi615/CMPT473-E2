import xml.etree.ElementTree as ET

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