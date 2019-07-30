

import os
import xml.etree.ElementTree as ET

file_name = 'bigSample.xml'
full_file = os.path.abspath(file_name)
print('input file is: '+ full_file)

qBank = ET.parse(full_file)
questionNames = qBank.findall('question/name/text')
# print(questionNames)
# for questionName in questionNames:
#     print(questionName.text)
questionTypes = qBank.findall('question')
for count, questionType in enumerate(questionTypes):
    print(count, questionType.attrib)
