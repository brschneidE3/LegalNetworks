
"""
ADD A DESCRIPTION OF WHAT THIS FILE IS FOR
"""
__author__ = 'brsch'

import datetime
import os
import helper_functions


proj_cwd = os.path.dirname(os.getcwd())
data_dir = proj_cwd + r'\data'


def create_jurisdiction_dict(directory):

    data_list = helper_functions.csv_to_list(directory, 'jurisdictions.csv', 1, 0)
    juris_dict = {}

    for row in data_list:
        new_juris = row_to_jurisdiction(row)
        new_abbrev = new_juris.abbrev
        juris_dict[new_abbrev] = new_juris

    return juris_dict


def row_to_jurisdiction(row):
    abbrev, name, count, jurisdiction, cit_abbrev, start_date, end_date, \
        use_string, mod_string = row

    if start_date == 'Unknown':
        start_date = None
    elif '-' in start_date:
        start_date = datetime.date(
            int(start_date.rsplit('-')[0]),
            int(start_date.rsplit('-')[1]),
            int(start_date.rsplit('-')[2])
            )
    elif '/' in start_date:
        start_date = datetime.date(
            int(start_date.rsplit('/')[2]),
            int(start_date.rsplit('/')[0]),
            int(start_date.rsplit('/')[1])
            )

    if end_date == 'Unknown':
        end_date = None
    elif '-' in end_date:
        end_date = datetime.date(
            int(end_date.rsplit('-')[0]),
            int(end_date.rsplit('-')[1]),
            int(end_date.rsplit('-')[2])
            )
    elif '/' in end_date:
        end_date = datetime.date(
            int(end_date.rsplit('/')[2]),
            int(end_date.rsplit('/')[0]),
            int(end_date.rsplit('/')[1])
            )

    in_use = True if use_string == 'Yes' else False
    mod_date_string = mod_string.rsplit('T')[0]
    mod_time_string = mod_string.rsplit('T')[1]
    mod_date_string = mod_date_string.rsplit('-')
    mod_time_string = mod_time_string.rsplit(':')
    modified = datetime.datetime(
        int(mod_date_string[0]),
        int(mod_date_string[1]),
        int(mod_date_string[2]),
        int(mod_time_string[0]),
        int(mod_time_string[1])
        )

    new_juris = JurisdictionClass(
        abbrev=abbrev,
        name=name,
        count=count,
        jurisdiction=jurisdiction,
        citation_abbrev=cit_abbrev,
        start_date=start_date,
        end_date=end_date,
        in_use=in_use,
        modified=modified)

    return new_juris


class JurisdictionClass:

    def __init__(self,
                 abbrev,
                 name=None,
                 count=None,
                 jurisdiction=None,
                 citation_abbrev=None,
                 start_date=None,
                 end_date=None,
                 in_use=None,
                 modified=None
                 ):
        """
        :param abbrev: STRING
        :param name: STRING
        :param count: INT
        :param jurisdiction: STRING
        :param citation_abbrev: STRING
        :param start_date: DATETIME DATE
        :param end_date: DATETIME DATE
        :param in_use: BOOLEAN
        :param modified: DATETIME DATETIME
        """

        self.abbrev = abbrev
        self.name = name
        self.count = count
        self.jurisdiction = jurisdiction
        self.citation_abbrev = citation_abbrev
        self.start_date = start_date
        self.end_date = end_date
        self.in_use = in_use
        self.modified = modified

    def __repr__(self):
        return "Abbreviation: \t %s \n" \
               "Name: \t \t \t %s \n" \
               "Count: \t \t \t %s \n" \
               "Jurisdiction: \t %s \n"\
               "Start date: \t %s \n"\
               "End date: \t \t %s \n"\
               "In use: \t \t %s \n"\
               % (self.abbrev, self.name, self.count, self.jurisdiction,
                  self.start_date, self.end_date, self.in_use)

jurisdiction_dict = create_jurisdiction_dict(data_dir)
