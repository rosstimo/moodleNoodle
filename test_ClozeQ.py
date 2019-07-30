import unittest
import ClozeQ

class TestClozeQ(unittest.TestCase):

    def test_ClozeStr(self):
        '''Instantiate From Moodle Cloze Formated String:'''
        myClozeQuestion = '{1:MRS:%50%Answer 1#Feedback 1~%50%Answer 2#Feedback 2~%-50%Answer 3#Feedback 3~%-50%Answer 4#Feedback 4}'
        question = ClozeQ(myClozeQuestion)

    def test_FromValues(self):
        '''Instantiate From Values:'''
        points = 1
        type = 'MC'
        responses = [[100,'right', 'good job'],[0,'wrong', 'sorry'],[0,'no way', 'really?']]
        question = ClozeQ.from_values(points, type, responses)

    def test_Update(self):
        pass

def testSample(self):
    '''Returns a string of various Moodle Cloze formatted questions'''
    sample = '''{105:MULTICHOICE:%100%Answer 1#Feedback 1~%50%Answer 2#Feedback 2~%0%Answer 3#Feedback 3}
    {1:SHORTANSWER:%100%blank#Feedback 1~%100%space#Feedback 2}
    {1:NUMERICAL:=0.6667:0.0001#Feedback for correct answer + or - .0001 ~%50%0.6667:.01#Feedback for half credit near correct answer in this case too much rounding error}'
    {1:NM:=4:1}
    {1:MULTICHOICE:=Answer 1#Feedback 1~Answer 2#Feedback 2~Answer 3#Feedback 3}
    {1:MULTICHOICE:Answer 1#Feedback 1~=Answer 2#Feedback 2~Answer 3#Feedback 3}
    {:MRS:Answer 1#Feedback 1~=Answer 2#Feedback 2~Answer 3#Feedback 3}
    {:MRS:%50%Answer 1#Feedback 1~%50%Answer 2#Feedback 2~%-50%Answer 3#Feedback 3~%-50%Answer 4#Feedback 4}'''
    return sample

if __name__ == '__main__':
    unittest.main()
