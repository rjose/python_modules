import utils.sectionize


# TODO: Add metadata

#-------------------------------------------------------------------------------
# Parses shortage chart text from file 'f' as a python dictionary.
#
# The text input should consist of three sections: a title, a demand, and a
# shortage. Here's an example:
#
#       =====title
#       	Shortage Chart (with shortage)
#       =====demand
#       	Track 1	20
#       	Track 2	35
#       =====shortage
#       	Apps	5
#       	Native	3
#       	QA	1
#
def parse(f):
    sections = utils.sectionize.sectionize(f)
    dataset = {}

    for s in ['demand', 'shortage']:
        dataset[s] = []
        for line in sections[s].split('\n'):
            fields = line.split('\t')
            dataset[s].append({'label': fields[0], 'value': float(fields[1])})

    result = {
            'command': 'chart',
            'title': sections['title'],
            'data': {
                'type': 'shortagechart',
                'dataset': dataset
            }
    }
    return result
