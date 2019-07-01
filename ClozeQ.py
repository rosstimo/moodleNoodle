import re
class ClozeQ:
    '''Moodle Cloze Embeded Question Tool

        more info here: https://docs.moodle.org/37/en/Embedded_Answers_(Cloze)_question_type

    Format Structure:

        The structure of each cloze sub-question is identical except the ':' seperator for accepted error in numerical answers:

            {               start the cloze sub-question with a bracket
            1               define a grade for each cloze by a number (optional). This used for calculation of question grading
            :MULTICHOICE:   define the type of cloze sub-question. The definition is bounded by ':'
            ~               is a separator between answer options
            =               marks a correct answer. It can also be percentage %100% or %50% or %0%
            :               !!! only for numerical to seperate correct answer and accepted error amount
            #               marks the beginning of an (optional) feedback message
            }               close the cloze sub-question at the end with a bracket

    Question Type Codes:

        Multiple Choice no Shuffle:

            MULTICHOICE or MC               represented as a dropdown menu in-line in the text
            MULTICHOICE_V or MCV            represented as a vertical column of radio buttons
            MULTICHOICE_H or MCH            represented as a horizontal row of radio-buttons
            MULTIRESPONSE or MR             represented as a vertical row of checkboxes
            MULTIRESPONSE_H or MRH          represented as a horizontal row of checkboxes

        Multiple Choice Shuffle sub questions:
            When the quiz question behavior shuffle option is set to YES, the following special multiple choice sub-questions elements will be shuffled:

            MULTICHOICE_S or MCS            represented as a dropdown menu in-line in the text
            MULTICHOICE_VS or MCVS          represented as a vertical column of radio buttons
            MULTICHOICE_HS or MCHS          represented as a horizontal row of radio-buttons
            MULTIRESPONSE_S or MRS          represented as a vertical row of checkboxes
            MULTIRESPONSE_HS or MRHS        represented as a horizontal row of checkboxes

        Short Answer:
            SHORTANSWER or SA or MW         case is unimportant
            SHORTANSWER_C or SAC or MWC     case must match

        Numerical Answers:
            NUMERICAL or NM                 Only option for numerical

    Examples:

        Multiple Choice example:
            Question text that student sees:
            {1:MULTICHOICE:%100%Answer 1#Feedback 1~%50%Answer 2#Feedback 2~%0%Answer 3#Feedback 3}

        Short Answer Example:
            Fill in the {1:SHORTANSWER:%100%blank#Feedback 1~%100%space#Feedback 2} to complete this sentence.

        Numerical Question Exmple:
            What is 2/3?
            {1:NUMERICAL:=0.6667:0.0001#Feedback for correct answer + or - .0001 ~%50%0.6667:.01#Feedback for half credit near correct answer in this case too much rounding error}

            The Cloze numerical type question will also include the accepted error value.
            The student will get the specifide points for an answer that is within the range of the crrect answer plus or minus the accepted error value.

            What is 2 + 2?
            {1:NM:=4:0} answer must be exactly 4
            {1:NM:=4:1} answer can be any thing from 3 to 5

    ###############################################################################

    initially started June 2019
    Based off of previous work creating deep question banks with vba script. This
    tool is intended to be an easy way to create, edit and maintain these large
    question banks.

    enjoy,

    Tim Rossiter
    rosstimo@isu.edu
    Idaho State University
    Robotics'''

    def __init__(self, cloze_Str):#TODO add verification that cloze question is properly formed. maybe raise exception or something
        '''Single Moodle Cloze Question.
        Properties Cloze formatted string, Question Points, Question Type,
        list of responses. If the question type is NUMERICAL or NM the answer
        field may contain the accepted error value seperated from the answer
        with a ':' in this format <answer:acceptedError> '''

        self._clozeStr = cloze_Str
        self._qPoints = self.getQPoints()
        self._type = self.getQType()
        self._responses = self.getQResponses()

    @property
    def qPoints(self):
        return self._qPoints
    @qPoints.setter
    def qpoints(self, updateStr):
        self._qPoints = updateStr
        self.clozeStr = self.makeClozeStr()

    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, updateStr):
        self._type = updateStr
        self.clozeStr = self.makeClozeStr()

    @property
    def responses(self):
        return self._responses
    @responses.setter
    def responses(self, updateStr):
        self._responses = updateStr
        self.clozeStr = self.makeClozeStr()

    @property
    def clozeStr(self):
        return self._clozeStr
    @clozeStr.setter
    def clozeStr(self, cloze_Str):
        self._clozeStr = cloze_Str
        self._qPoints = self.getQPoints()
        self._type = self.getQType()
        self._responses = self.getQResponses()

    @classmethod
    def from_values(cls, qPoints, type, responses):
        '''Create instance from values'''
        responseStr =''
        for r in responses:
            responseStr += '~%{}%{}#{}'.format(str(r[0]),r[1],r[2])
        return cls('{' + str(qPoints) +':' + type + ':' + responseStr + '}')

    def makeClozeStr(self):
        '''property attribute: returns Moodle Cloze formatted string'''
        responseStr =''
        print(self.responses)
        for r in self.responses:
            print(self.r)
            responseStr += '~%{}%{}#{}'.format(str(r[0]),r[1],r[2])
        return '{' + str(self.qPoints) +':' + self.type + ':' + responseStr + '}'

    def getQPoints(self):
        '''Returns default points for the question. '' will defualt to 1 point.'''#TODO Should empty points string be set to 1? Moodle won't care.
        pattern = re.compile(r'{(\d*):')
        matches = pattern.findall(self.clozeStr)
        return matches[0]

    def getQType(self):
        '''returns Moodle Cloze question type code as a string'''
        pattern = re.compile(self.getQPoints() + r':(\w+):')
        matches = pattern.findall(self.clozeStr)
        return matches[0]

    def getQResponses(self):
        '''returns list of graded response values in this format ('points', 'answer' , 'acceptable range', 'feedback') '''#TODO still haven,t handeled acceptabe range for NM questions
        return self.getResponse(self.getQResponseStr())

    def getQResponseStr(self):
        '''returns raw response string'''
        pattern = re.compile(r':' + self.getQType() + r':(.+)}')
        matches = pattern.findall(self.clozeStr)
        return matches[0]

    def getResponse(self, responseStr):#TODO: verify if this can be done more efficiently with regular expressions
        ''' Takes a string of possible responses stripped from Moodle Cloze formatted string and seperates: answer points, answer, acceptable error value in a NUMERICAL or NM type, and feedback'''
        final = []
        responses = responseStr.split('~')
        for response in responses:
            temp = []
            if response != '':
                if response[0] == '=':
                    temp.append('100')
                    nut = response[1:]
                elif response[0] == '%':
                    findPnts = response.split('%')
                    temp.append(findPnts[1])
                    nut = findPnts[2]
                else:
                    temp.append('0')
                    nut = response
                if '#' in nut:
                    cracked = nut.split('#')
                    temp.append(cracked[0])
                    temp.append(cracked[1])
                else:
                    temp.append(nut)
                    temp.append('')
                final.append(temp)
        return final

    def showQuestion(self):
        '''prints a deconstructed view of a Moodle Cloze Question'''
        print('')
        print(self.clozeStr)
        print('')
        print('-- Question Points:      ' + self.getQPoints())
        print('   Question Type:        ' + self.getQType())
        print('   Question Responses:')
        for q in self.getQResponses():
            print('    -- Points:           ' + q[0])
            print('       Response:         ' + q[1])
            print('       Feedback:         ' + q[2])

    def __repr__(self):
        return "CloseQ('{}', '{}', '{}')".format(self.qPoints, self.type ,self.responses)

    def __str__(self):
        return '{} - {} - {}'.format(self.qPoints, self.type ,self.responses)

    def usage(self):
        '''
        Usage Examples:

        Instantiate From Moodle Cloze Formated String:

            myClozeQuestion = '{1:MRS:%50%Answer 1#Feedback 1~%50%Answer 2#Feedback 2~%-50%Answer 3#Feedback 3~%-50%Answer 4#Feedback 4}'
            question_1 = ClozeQ(myClozeQuestion)

        Instantiate From Values:

            points = 1

            type = 'MC'
            responses = [[100,'right', 'good job'],[0,'wrong', 'sorry'],[0,'no way', 'really?']]
            question_2 = ClozeQ.from_values(points, type, responses)
        '''

if __name__ == '__main__' :

    docStr = ClozeQ.__doc__.splitlines()
    for line in docStr:
        print(line)

    docStr = ClozeQ.usage.__doc__.splitlines()
    for line in docStr:
        print(line)
