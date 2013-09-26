import datetime
import re

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

def str_to_date(datestring):
    if datestring == "":
        return None
    result = datetime.datetime.strptime(datestring, "%m/%d/%Y")
    return result

def expand_dates(dates_list):
    result = []
    for v_range in dates_list:
        num_days = (v_range[1] - v_range[0]).days + 1
        for i in range(num_days):
            delta = datetime.timedelta(days=i)
            result.append(v_range[0] + delta)

    return result

def get_formatted_vacation(name, vacations):
    for v in vacations:
        if re.match(name, v):
            days = [d.strftime("%b %e, %Y") for d in vacations[v]]
            return ":".join(days)
    return ""

def parse_vacation_data(name, start, end, note, condition_vacation):
    result = [None, None, note]
    if start:
        result = [str_to_date(start), str_to_date(end), note]
    else:
        result = condition_vacation(name, note)
    return result
