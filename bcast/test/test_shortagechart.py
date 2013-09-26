import io
import unittest
import bcast.shortagechart

happy_input1 = """=====title
	ShortageChart Title
=====demand
	Track 1	20
	Track 2	35
=====shortage
	Apps	5
	Native	3
	QA	1"""

class TestShortageChart(unittest.TestCase):

    def test_format_text1(self):
        input = io.StringIO(happy_input1)
        result = bcast.shortagechart.parse(input)
        self.assertEqual("ShortageChart Title", result['title'])
        demand = result['data']['dataset']['demand']
        self.assertEqual("Track 1", demand[0]['label'])
        self.assertEqual("20", demand[0]['value'])
        # TODO: Test other sections
        return


if __name__ == '__main__':
    unittest.main()
