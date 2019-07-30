

from bs4 import BeautifulSoup
import requests
import csv

class MoodleXML:

    def __init__(self, filename):
        '''Moodle XML test bank'''
        self.moodle_xml = self.read_xml(filename)
        # with open(xml_file_name,'r', encoding='utf-8') as self._xml_file:
        #     self.moodle_xml = BeautifulSoup(self._xml_file, 'xml', from_encoding='utf-8')



            # content = self._xml_file.readlines()
        #     try:
        #         for num, line in enumerate(self._xml_file):
        #             junk = num
        #         print('Hooray!', junk)
        #     except:
        #         print(num, line)


        # try:
        #     with open(xml_file_name,'r', encoding='utf-16') as self._xml_file_name:
        #         # self.moodle_xml = BeautifulSoup(self._xml_file_name, 'lxml')
        #         self.moodle_xml = BeautifulSoup(self._xml_file_name, 'xml', from_encoding='utf-16')
        # except:
        #     print('Something went wrong.' )
        # finally:
        #     pass


    def read_xml(self, filename):
        with open(filename,'r') as self._xml_file:
            xml_file = BeautifulSoup(self._xml_file, 'xml')
        return xml_file

    def write_xml(self, filename):
        pass

    def write_csv(self, filename):
        pass

    def write_html(self, filename):
        pass

    def getCategory(self):
        for question in self.moodle_xml.find_all('question'):
            print(question.attribute)
        return self.moodle_xml.find_all('question')

    def getType(self):
        pass

    def getName(self):
        pass

    def getQestionText(self):
        pass

testXML = MoodleXML('sample.xml')

print(testXML.getCategory())
