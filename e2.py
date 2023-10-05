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




def CsvtoJsonArg(input,output,testNum, D,S,T,sep):
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



def test():
    for idx, testcase in enumerate(test_cases):
        CsvtoJsonArg(f'TestData{testcase["Test No."]}.csv',f'TestJson{testcase["Test No."]}.json',testcase["Test No."], testcase["D_OPTION"],testcase["S_OPTION"], testcase["T_OPTION"], testcase['FIELD_SEPARATOR'] )

    for x in range(1,11):
        print(f'test{x}:')
        out = f'Output/TestJson{x}.json'
        exp = f'ExpectedOutput/Output{x}.json'
        result = filecmp.cmp(out,exp)  
        print(result)

    



if __name__ == "__main__":
    test()