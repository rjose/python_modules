#-------------------------------------------------------------------------------
# Parses piechart text from file 'f' as a python dictionary.
#
# The first line of the text is taken to be the title of the chart. The
# following lines should consist of two fields separated by a tab. The first
# field is the label of the field; the second is the value. For example:
#
#       This is the title of the chart
#       Label1\t10
#       Label2\t20
#
def parse(f):
        # Read title and data set
        title = f.readline()
        dataset = []
        for line in f.readlines():
                fields = line.split("\t")
                dataset.append({'value': fields[1], 'label': fields[0]})

        # Structure result and conver to JSON
        result = {
          'command': 'chart',
          'title': title,
          'data' : {
             'type': 'piechart',
             'dataset': dataset
             }
         }
        return result
