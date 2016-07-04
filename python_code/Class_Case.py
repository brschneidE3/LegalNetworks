import os
import sys
import json
import datetime

__author__ = 'idc9'

cwd = os.getcwd()
data_dir = cwd + r'..\data'


# Given the juristidction, file type and root path to data
# Returns a list of case ids in that jurisdiction
def get_cases_in_jurisdiction(juris_abv='nced', file_type='opinions',
                              data_dir='../data'):

    # path leading to the jurisdiction files
    path = data_dir + '/' + file_type + '/' + juris_abv + '/'

    # TODO: throw an exception
    # Check that the directory exists
    if not os.path.isdir(path):
        print 'not a legal path'
        return []
    else:
        return [int(f.split('.json')[0]) for f in os.listdir(path)]

# Cases in the nced
nced_case_ids = get_cases_in_jurisdiction('nced')


class Case:
    """
    Case class that store the metadata for a case node
    Requires the opinion and cluster files
    Stores: case_name, case_id, date, case text
    """
    def __init__(self, op_file, cl_file):

        # Open the cluster and opinion json files
        with open(cl_file) as data_file:
            cl_data_temp = json.load(data_file)

        with open(op_file) as data_file:
            op_data_temp = json.load(data_file)

        # TODO: do this more succinctly
        # Convert to utf8 from unicode
        cl_data = {}
        for k in cl_data_temp.keys():
            value = cl_data_temp[k]
            if k == 'opinions_cited':
                cl_data['opinions_cited'] = [v.encode('utf8') for v in value]
            elif type(value) == unicode:
                cl_data[k.encode('utf8')] = value.encode('utf8')
            else:
                cl_data[k.encode('utf8')] = value

        op_data = {}
        for k in op_data_temp.keys():
            value = op_data_temp[k]
            if k == 'opinions_cited':
                op_data['opinions_cited'] = [v.encode('utf8') for v in value]
            elif type(value) == unicode:
                op_data[k.encode('utf8')] = value.encode('utf8')
            else:
                op_data[k.encode('utf8')] = value

        for k in cl_data.keys():
            if k == 'case_name':
                self.case_name = cl_data[k]

            if k == 'citation_id':
                self.case_id = cl_data[k]

            if k == 'date_filed':
                # TODO: make sure date is always in this format
                date_explode = cl_data['date_filed'].split('-')
                file_date = datetime.date(int(date_explode[0]),
                                          int(date_explode[1]),
                                          int(date_explode[2]))
                self.date = file_date

        # Get the case text
        text = op_data['html']
        if len(text) == 0:
            text = op_data['html_with_citations']
        elif len(text) == 0:
            text = op_data['plain_text']
        elif len(text) == 0:
            text = op_data['html_lawbox']
        elif len(text) == 0:
            text = ''
            print('case ' + str(i) + ' has no text')

        self.text = text

    def __repr__(self):
        return "Name: \t %s \n"\
               "Id \t %s \n"\
               "Date \t %s \n"\
                % (self.case_name, self.case_id, self.date)

# Example code to load a case
cl_file = data_dir + '/clusters/nced/1361899.json'
op_file = data_dir + '/opinions/nced/1361899.json'

case = Case(op_file, cl_file)
