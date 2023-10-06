import os
import io
import filecmp
import xml.etree.ElementTree as ET
import csv
import shutil

inputPath = 'TestData/'
outputPath = "Output/"
expectedPath = 'ExpectedOutput'


albums = ['SOS', 'Nicole', '"Pure BS"', 'Nurture']
artists = ['SZA', 'NIKI', '"Blake Shelton"', '"Porter Robinson"']
genres = ['R&B', 'Pop', 'Country', 'EDM']
years = [2022, 2022, 2021, 2007]
recs = [True, True, False, True]

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

# Generate input files
def generateInput ():
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


def CsvtoJsonArg(input,output,testNum, D,S,T,sep, validInput, validOutput):
    options = ''    
    fsep = ''
    if(sep == 'comma'):
        fsep += "','"
    if(sep == 'tab'):
        fsep += "'	'"
    if(sep == 'colon'):
        fsep += "':'"


    if(D == 'true'):
        options += " -d "
    if (S =='true'):
        options += f" -s {fsep} "
    if (T == 'true'):
        options += " -t "
    arg = f'csv2json {options} {inputPath}{input} {outputPath}{output}'

    os.system(arg)

    #Expected message file generator
    expectedMessageFile = "ExpectedMessage/" + f'ExpectedMessage{testNum}.txt'
    file = open(expectedMessageFile, "w")
    msgs = [f'Case{testNum}', "Program Output and Expected Output match"]
    msgs_2 = [f'Case{testNum}', "Invalid Input File"]
    msgs_3 = [f'Case{testNum}', "Invalid Output File"]

    if validInput and validOutput=='false':
      for msg1 in msgs_3:
        file.write(msg1 + '\n')
    elif validInput == 'false' and validOutput:
      for msg2 in msgs_2:
        file.write(msg2 + '\n')
    else:
      for msg in msgs:
        file.write(msg + '\n')
    return arg


def compareMessages(testNum, messageOutputFilePath, expectedMessagePath):
    if filecmp.cmp(messageOutputFilePath, expectedMessagePath):
        msg = f'Test Case{testNum}: Passed: Output message matched the expected out message.\n'
    else:
        msg = f'Test Case{testNum}: Failed: Output message did not match the expected out message.\n'
    print(msg)



def test():
    for idx, testcase in enumerate(test_cases):
        wrong = ''
        if testcase["VALID_INPUT"] == "false":
            wrong = 'wrong'
        if testcase['IS_FILE_EMPTY'] == 'true':
            CsvtoJsonArg(f'TestData3{wrong}.csv',f'TestJson{testcase["Test No."]}.json',testcase["Test No."], testcase["D_OPTION"],testcase["S_OPTION"], testcase["T_OPTION"], testcase['FIELD_SEPARATOR'], testcase['VALID_INPUT'], testcase['VALID_OUTPUT'])
        elif testcase['BOOL_NUM'] == 'true':
            CsvtoJsonArg(f'TestData2{wrong}.csv',f'TestJson{testcase["Test No."]}.json',testcase["Test No."], testcase["D_OPTION"],testcase["S_OPTION"], testcase["T_OPTION"], testcase['FIELD_SEPARATOR'], testcase['VALID_INPUT'], testcase['VALID_OUTPUT'])
        else:
            CsvtoJsonArg(f'TestData1{wrong}.csv',f'TestJson{testcase["Test No."]}.json',testcase["Test No."], testcase["D_OPTION"],testcase["S_OPTION"], testcase["T_OPTION"], testcase['FIELD_SEPARATOR'], testcase['VALID_INPUT'], testcase['VALID_OUTPUT'])


    
        outputMessage = "TestDataOutputMessage"
        out = f'Output/TestJson{idx+1}.json'
        exp = f'ExpectedOutput/Output{idx+1}.json'
        if filecmp.cmp(out,exp):
           msg = f'Case{testcase["Test No."]}' + '\n' "Program Output and Expected Output match"
        else:
           msg = f'Case{testcase["Test No."]}' + '\n' "Program Output and Expected Output do not match"

        with open(outputMessage + f'/OutputMessage{idx+1}.txt', 'w') as file:
            file.write((msg + '\n'))
        outputMessagePath = outputMessage + f'/OutputMessage{idx+1}.txt'
        expectedMessagePath = "ExpectedMessage/" + f'ExpectedMessage{idx+1}.txt'
        if filecmp.cmp(outputMessagePath, expectedMessagePath):
            print(f'Test Case{idx+1}: Passed')
        else:
            print(f'Test Case{idx+1}: Failed') 

    
if __name__ == "__main__":
    generateInput()
    test()