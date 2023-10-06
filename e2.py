import os
import io
import filecmp
import xml.etree.ElementTree as ET

inputPath = 'TestData/'
outputPath = "Output/"
expectedPath = 'ExpectedOutput'


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

def CsvtoJsonArg(input,output,testNum, D,S,T,sep, validInput, validOutput):
    options = ''    
    fsep = ''
    if(sep == 'comma'):
        fsep += "','"
    if(sep == 'tab'):
        fsep += "'  '"
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

        CsvtoJsonArg(f'TestData{testcase["Test No."]+wrong}.csv',f'TestJson{testcase["Test No."]}.json',testcase["Test No."], testcase["D_OPTION"],testcase["S_OPTION"], testcase["T_OPTION"], testcase['FIELD_SEPARATOR'], testcase['VALID_INPUT'], testcase['VALID_OUTPUT'])
    
        outputMessage = "TestDataOutputMessage"
        out = f'Output/TestJson{idx+1}.json'
        exp = f'ExpectedOutput/Output{idx+1}.json'
        if filecmp.cmp(out,exp):
           msg = f'Case{testcase["Test No."]}' + '\n' "Program Output and Expected Output match"
        else:
           msg = f'Case{testcase["Test No."]}' + '\n' "Program Output and Expected Output do not match"

        with open(outputMessage + f'/OutputMessage{idx+1}.txt', 'w') as file:
            file.write((msg + '\n\n'))  

    
if __name__ == "__main__":
    test()