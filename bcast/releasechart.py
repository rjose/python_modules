import utils.sectionize


# TODO: Split into chart data and metadata



#-------------------------------------------------------------------------------
# Parses shortage chart text from file 'f' as a python dictionary.
#
# The text input should consist of three sections: a title, release dates, and a
# feature dates (name, expected, target). Here's an example:
#
#       =====title
#       	Demo ReleaseChart
#       =====release dates
#       	Aug 30, 2013
#       	Oct 15, 2013
#       	Nov 15, 2013
#       =====features
#       	Feature1	Aug 15, 2013	Aug 30, 2013
#       	Feature2	Aug 25, 2013	Aug 30, 2013
#       	Feature3	Aug 15, 2013	Aug 30, 2013
#       	Awesomeness	Aug 25, 2013	Aug 30, 2013
#       	2x Awesomeness	Sep 15, 2013	Oct 15, 2013
#
# The target date is what we're shooting at for each feature. The expected date
# should be the best estimate of where this feature will land.
#
def parse(f):
    sections = utils.sectionize.sectionize(f)
    dataset = {'releaseDates': [], 'features': []}

    # Add release dates
    for line in sections['release dates'].split('\n'):
        fields = line.split('\t')
        dataset['releaseDates'].append(fields[0])

    # Add features
    for line in sections['features'].split('\n'):
        fields = line.split('\t')
        dataset['features'].append({
            'name': fields[0],
            'expected': fields[1],
            'target': fields[2]
        })

    result = {
            'command': 'chart',
            'title': sections['title'],
            'data': {
                'type': 'releasechart',
                'dataset': dataset
            }
    }
    return result
