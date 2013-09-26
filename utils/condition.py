import re

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

def check_streams(stream_names, streams):
        missing_streams = [s for s in stream_names if s not in streams]
        if missing_streams != []:
                raise Exception("Missing required streams", missing_streams)

def pack_string(labels, values):
    items = []
    for i in range(len(labels)):
        if values[i]:
            items.append(labels[i] + ":" + values[i])
    result = ",".join(items)
    return result

def condition_string(string, pattern_map):
    for pattern in pattern_map.keys():
        if re.match(pattern, string):
            return pattern_map[pattern]
    return string

def condition_user_input(input):
    result = re.sub("[\:\n]", "-", input)
    result = re.sub("'", "`", result)
    return result

def construct_header_map(headers, row):
    result = {}

    row_fields = row.split("\t")
    for h in headers:
        for i in range(len(row_fields)):
            if row_fields[i] == h:
                result[h] = i

    missing_headers = []
    for h in headers:
        if h not in result:
            missing_headers.append(h)
    if missing_headers != []:
        raise Exception("Missing some headers", missing_headers)
    return result
