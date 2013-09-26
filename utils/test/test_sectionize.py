import unittest
import utils.sectionize as sectionize
import io

happy_input1 = """=====title
	ShortageChart Title
=====demand
	Track 1	20
	Track 2	35
=====shortage
	Apps	5
	Native	3
	QA	1"""

class TestSectionize(unittest.TestCase):

    def test_sectionize1(self):
        input = io.StringIO(happy_input1)
        result = sectionize.sectionize(input)
        self.assertEqual("ShortageChart Title", result['title'])
        return


if __name__ == '__main__':
    unittest.main()
