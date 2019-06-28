import re
class ClozeQ:
    '''Cloze Embeded Question Generator

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

    def __init__(self, questionPoints, questionType, questionResponses=None):
        '''Single Moodle Cloze Question.
        Properties Cloze formatted string, Question Points, Question Type,
        list of responses. If the question type is NUMERICAL or NM the answer
        field may contain the accepted error value seperated from the answer
        with a ':' in this format <answer:acceptedError> '''
        #self.clozeStr = makeClozeStr(questionPoints, questionType, responses)
        self.questionPoints = questionPoints
        self.questionType = questionType
        self.questionResponses = questionResponses


    @classmethod
    def from_clozeStr(cls, clozeStr):
        #cls.clozeStr = clozeStr
        x = cls.getQPoints(cls, clozeStr)
        y = cls.getQType(cls, clozeStr)
        z = cls.getQResponses(cls, clozeStr)
        return cls(x, y, z)

        # def clozeStr(self):
        #     pass
        #
        # @clozeStr.setter
        # def clozeStr(self, clozeStr):
        #     pass

    def getQuestions(self, clozeStr):
        '''returns list of all cloze formatted questions in a string'''
        pattern = re.compile(r'{.+}')
        matches = pattern.findall(clozeStr)
        return matches

    def getQPoints(self, clozeStr):
        '''Returns defailt poinst for the question. '' will defualt to 1 point.'''
        pattern = re.compile(r'{\d*')
        matches = pattern.findall(clozeStr)
        return matches[0].replace('{','')#TODO: see if there is a cleanear way to return what is between the digits only

    def getQType(self, clozeStr):
        '''returns Moodle Cloze question type code as a string'''
        pattern = re.compile(r':\w+:')
        list_matches = pattern.findall(clozeStr)
        return list_matches[0].replace(':','')#TODO: see if there is a cleanear way to return what is between the :'s only

    def getQResponses(self, clozeStr):
        '''returns list of graded response values in this format ('points', 'answer' , 'acceptable range', 'feedback') '''
        pattern = re.compile(r':\w+:.+}')
        matches = pattern.findall(clozeStr)
        for i, match in enumerate(matches):
            s = re.search(r':' + getQType(match) + ':', match)
            e = re.search(r'}', match)
            responseStr = match[s.end():e.end()-1]
        return getResponse(responseStr)#TODO: return respons string

    def getQResponseStr(self, clozeStr):
        '''returns raw response string'''
        pattern = re.compile(r':\w+:.+}')
        matches = pattern.findall(clozeStr)
        for i, match in enumerate(matches):
            s = re.search(r':' + getQType(match) + ':', match)
            e = re.search(r'}', match)
            responseStr = match[s.end():e.end()-1]
        return responseStr

    def getResponse(self, responseStr):#TODO: take getResponseStr() as an arg
        ''' Takes a string of possible responses stripped from Moodle Cloze formatted string and seperates: answer points, answer, acceptable error value in a NUMERICAL or NM type, and feedback'''
        final = []
        responses = responseStr.split('~')
        for response in responses:
            temp = []
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

    def makeClozeStr(self):
        '''returns Moodle Cloze formatted string'''
        responseStr =''
        for r in self.questionResponses:
            responseStr += '%{}%{}#{}'.format(str(r[0]),r[1],r[2])
        return '{' + str(self.questionPoints) +':' + self.questionType + ':' + responseStr + '}'

    def showQuestion(self, question):
        '''prints a deconstructed view of a Moodle Cloze Question'''
        print('')
        print(question)
        print('')
        print('-- Question Points:      ' + getQPoints(question))
        print('   Question Type:        ' + getQType(question))
        print('   Question Responses:')
        for q in getQResponses(question):
            print('    -- Points:           ' + q[0])
            print('       Response:         ' + q[1])
            print('       Feedback:         ' + q[2])

    def testSample(self):
        '''Returns a string of various Moodle Cloze formatted questions'''
        sample = '''{105:MULTICHOICE:%100%Answer 1#Feedback 1~%50%Answer 2#Feedback 2~%0%Answer 3#Feedback 3}
        {1:SHORTANSWER:%100%blank#Feedback 1~%100%space#Feedback 2}
        {1:NUMERICAL:=0.6667:0.0001#Feedback for correct answer + or - .0001 ~%50%0.6667:.01#Feedback for half credit near correct answer in this case too much rounding error}' +
        {1:NM:=4:1}
        {1:MULTICHOICE:=Answer 1#Feedback 1~Answer 2#Feedback 2~Answer 3#Feedback 3}
        {1:MULTICHOICE:Answer 1#Feedback 1~=Answer 2#Feedback 2~Answer 3#Feedback 3}
        {:MRS:Answer 1#Feedback 1~=Answer 2#Feedback 2~Answer 3#Feedback 3}
        {:MRS:%50%Answer 1#Feedback 1~%50%Answer 2#Feedback 2~%-50%Answer 3#Feedback 3~%-50%Answer 4#Feedback 4}'''
        return sample

    def __repr__(self):
        return "CloseQ('{}', '{}', '{}')".format(self.questionPoints, self.questionType ,self.questionResponses)

    def __str__(self):
        return '{} - {} - {}'.format(self.questionPoints, self.questionType ,self.questionResponses)
    # if __name__ == '__main__' :
    #     pass

'''TESTING BELOW HERE'''
junk = '{:MRS:%50%Answer 1#Feedback 1~%50%Answer 2#Feedback 2~%-50%Answer 3#Feedback 3~%-50%Answer 4#Feedback 4}'
#test = ClozeQ.from_clozeStr(junk)
points = 1
type = 'MC'
responses = ((100,'right', 'good job'),(0,'wrong', 'sorry'),(0,'no way', 'really?'))
test2 = ClozeQ(points, type, responses)
#print(test2.questionPoints, test2.questionType ,test2.responses)
print(test2.__repr__)
print(test2.__str__)
print(test2.questionPoints, test2.questionType, test2.questionResponses)
print(test2.makeClozeStr())
# test.clozeStr.showQuestio()

# clozeQuestions = getQuestions(testSample())
# for q in clozeQuestions:
#     showQuestion(q)
