import re
class ClozeQ():
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



    def __init__(self, questionPoints, questionType, acceptedError, responses=None):
        self.questionPoints = questionPoints
        self.questionType = questionType
        if responses is None:
            self.responses = []
        else:
            self.responses = responses
        self.acceptedError = acceptedError


    @property
    def clozeStr(self):
        responsStr=''
        for item in reponsees:
            responsStr += responses(str(item))+':' + str(self.acceptedError)

        return '{}:{}:{}{}'.format(self.questionPoints, self.questionType)

test = ClozeQ(1,'NM', 1,('%100%',4) )

# some test cases
myAnswers = ('=Some Answer#feedback', '%50%half right#a little feedback', '=4:1#close enough', '%100%4:1', 'wrong#close enough', '~nope#try again~=yep#you got it!')
str_1 = '{1:MULTICHOICE:%100%Answer 1#Feedback 1~%50%Answer 2#Feedback 2~%0%Answer 3#Feedback 3}'
str_2 = '{1:SHORTANSWER:%100%blank#Feedback 1~%100%space#Feedback 2}'
str_3 = '{1:NUMERICAL:=0.6667:0.0001#Feedback for correct answer + or - .0001 ~%50%0.6667:.01#Feedback for half credit near correct answer in this case too much rounding error}'
str_4 = '{1:NM:=4:1}'
str_5 = '{1:MULTICHOICE:=Answer 1#Feedback 1~Answer 2#Feedback 2~Answer 3#Feedback 3}'
str_6 = '{1:MULTICHOICE:Answer 1#Feedback 1~=Answer 2#Feedback 2~Answer 3#Feedback 3}'
str_7 = '{:MRS:Answer 1#Feedback 1~=Answer 2#Feedback 2~Answer 3#Feedback 3}'
str_8 = '{:MRS:%50%Answer 1#Feedback 1~%50%Answer 2#Feedback 2~%-50%Answer 3#Feedback 3~%-50%Answer 4#Feedback 4}'

str_10 = '''{1:MULTICHOICE:%100%Answer 1#Feedback 1~%50%Answer 2#Feedback 2~%0%Answer 3#Feedback 3}'+
'{1:SHORTANSWER:%100%blank#Feedback 1~%100%space#Feedback 2}'
'{1:NUMERICAL:=0.6667:0.0001#Feedback for correct answer + or - .0001 ~%50%0.6667:.01#Feedback for half credit near correct answer in this case too much rounding error}' +
'{1:NM:=4:1}'+
'{1:MULTICHOICE:=Answer 1#Feedback 1~Answer 2#Feedback 2~Answer 3#Feedback 3}'+
'{1:MULTICHOICE:Answer 1#Feedback 1~=Answer 2#Feedback 2~Answer 3#Feedback 3}'+
'{:MRS:Answer 1#Feedback 1~=Answer 2#Feedback 2~Answer 3#Feedback 3}'+
'{:MRS:%50%Answer 1#Feedback 1~%50%Answer 2#Feedback 2~%-50%Answer 3#Feedback 3~%-50%Answer 4#Feedback 4}'''

def getQuestions(clozeStr):
    '''returns list of all cloze formattes questions in a string'''
    pattern = re.compile(r'{.+}')
    matches = pattern.findall(clozeStr)
    return matches

def getQPoints(clozeStr):
    '''Returns defailt poinst for the question. '' will defualt to 1 point.'''
    pattern = re.compile(r'{\d*')
    matches = pattern.findall(clozeStr)
    return matches[0].replace('{','')#TODO: see if there is a cleanear way to return what is between the digits only

def getQType(clozeStr):
    '''returns Moodle Cloze question type code as a string'''
    # flag = False
    #qType = ''
    # for char in clozeStr:
    #     if char == ':' :
    #         flag = not flag
    #     elif char != ':' and flag == True:
    #         qType += char
    #     elif char and flag == True:
    #         break
    pattern = re.compile(r':\w+:')
    list_matches = pattern.findall(clozeStr)
    return list_matches[0].replace(':','')#TODO: see if there is a cleanear way to return what is between the :'s only

def getQResponses(clozeStr):
    '''returns list of graded response values in this format ('points', 'answer' , 'acceptable range', 'feedback') '''
    pattern = re.compile(r':\w+:.+}')
    matches = pattern.findall(clozeStr)
    for i, match in enumerate(matches):
        s = re.search(r':' + getQType(match) + ':', match)
        e = re.search(r'}', match)
        responseStr = match[s.end():e.end()-1]
        junk = getResponse(responseStr)
    return matches

def getResponse(responseStr):
    ''' Takes a string of possible responses stripped from Moodle Cloze formatted string and seperates: answer points, answer, acceptable error value in a NUMERICAL or NM type, and feedback'''

    final = []
    responses = responseStr.split('~')
    for response in responses:
        temp = []
        print(response)
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
        print(nut)
        if '#' in nut:
            cracked = nut.split('#')
            temp.append(cracked[0])
            temp.append(cracked[1])
        else:
            temp.append(nut)
        final.append(temp)
    print(final)
    return None

def wrapQuestion():
    '''returns Moodle Cloze formatted string'''
    pass
    #return
clozeQuestions = getQuestions(str_10)
for q in clozeQuestions:
    print('')
    print(q)
    print('')
    print('Question Points:    ' + getQPoints(q))
    print('Question Type:      ' + getQType(q))
    print('Question Responses:' , getQResponses(q))

#
# pattern = re.compile(r':\w+:')
# matches = pattern.finditer(str_1)
# list_matches = pattern.findall(str_1)
# for match in matches:
#     print(match)
# for match in list_matches:
#     print(match)
# print(len(list_matches))
# first_match = pattern.search(str_1)
# print(first_match)

'''
#parse up possible response combinationd. assumes prior extraction from cloze formated string
for answer in myAnswers:
    points = ''
    ans = ''
    accErr = ''
    feedback = ''
    #junk = answer.split('=')
    #for i in enumerate(junk):
    #    print(i)
    #break

    if '=' in answer:
        aList = answer.split('=')
        points = '100'
    elif '%100%'in answer:
        aList = answer.split('%100%')
        points = '100'
    elif "%" in answer[0] and "%" in answer[2:4]:
        aList = answer.split('%')
    else: #TODO:I think Moodle will error if there is no 100% answer not sure. some MR or MRS might not have them. if so all blank strings here should be fine.
        aList = ('', '', answer)  #('','$$!No right answer found!',answer)
        #points = '0'

    print(answer)
    for i in enumerate(aList):
        print(i)

    fList = aList[1].split('#')
    print('     ',aList)
    for i in enumerate(fList):
        print('     ',i)

    #ans = fList[0]
    #feedback = fList[1]

    if "%" in answer[0] and "%" in answer[2:4]:
        pList = answer.split('%')
        points = pList[1]
        ans = pList[2]
    else:
        pList = ('', '')
        points = '0'

    print(answer)
    for i in enumerate(pList):
        print(i)


    if "#" in ans:
        fList = ans.split('#')
        feedback = fList[len(fList)-1]
        ans = fList[0]
    if ":" in ans:
        aList = ans.split(':')
        ans = aList[0]
        accErr = aList[1]

    #print('points: ' + points,' - Answer: ' + ans, ' - Accepted Error: ' + accErr, ' - FeedBack: ' + feedback)

#print(test.questionType)
'''
