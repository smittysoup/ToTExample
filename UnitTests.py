from BracketParser import BracketParser as b
import unittest


class TestParser(unittest.TestCase):
    def setUp(self):
        self.output={}
        
    def test_case_1(self):
        self.output["node_tasks"] ="[GOAL]: this is the goal"
        result = b(self.output).parse()
        self.assertEqual(result, {"goal": "this is the goal"})

    def test_case_2(self):
        self.output["node_tasks"] ="GOAL: this is the goal"
        result = b(self.output).parse()
        self.assertEqual(result, {"goal": "this is the goal"})

    def test_case_3(self):
        self.output["node_tasks"] ="[GOAL]: \n             this is the goal"
        result = b(self.output).parse()
        self.assertEqual(result, {"goal": "this is the goal"})
        
    def test_case_5(self):
        self.output["node_tasks"] ="[GOAL HERE]: \n             this is the goal"
        result = b(self.output).parse()
        self.assertEqual(result, {"goal here": "this is the goal"})
        
    def test_case_6(self):
        self.output["node_tasks"] ="\n\n   [GOAL HERE]: \n             this is the goal"
        result = b(self.output).parse()
        self.assertEqual(result, {"goal here": "this is the goal"})
    
    def test_case_4(self):
        self.output["node_tasks"] ="[GOAL]: \n             this is the goal\n    [GOAL]: \n             this is the goal "
        result = b(self.output).parse()
        self.assertEqual(result, {"goal": "this is the goal","goal": "this is the goal"})
        
if __name__ == '__main__':
    unittest.main()