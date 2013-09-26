import utils.sectionize


# TODO: Split into chart data and metadata

#-------------------------------------------------------------------------------
# Parses shortage chart text from file 'f' as a python dictionary.
#
# The text input should consist of two sections: a title and a points section.
# Here's an example:
#
#        =====title
#        	Demo Quadchart
#        =====points
#        	Alpha	5	20
#        	Beta	450	90
#        	Gamma	250	50
#        	Upsilon	100	30
#
def parse(f):
    sections = utils.sectionize.sectionize(f)
    dataset = []

    for line in sections['points'].split('\n'):
        fields = line.split('\t')
        dataset.append({'name': fields[0],
                        'effort': float(fields[1]),
                        'value': float(fields[2])})

    result = {
            'command': 'chart',
            'title': sections['title'],
            'data': {
                'type': 'quadchart',
                'dataset': dataset
            }
    }
    return result
