__author__ = 'brendan'

import helper_functions
import networkx as nx
import matplotlib.pyplot as plt
import datetime
from operator import itemgetter
import numpy as np
import os

proj_cwd = os.path.dirname(os.getcwd())
data_dir = proj_cwd + r'\data'

###############
# BUILD A GRAPH
###############
# Load data from the CSVs
edgelist_data = helper_functions.csv_to_list(data_dir + r'\scotus',
                                             'citations_sublist.csv',
                                             1, 0)
node_data = helper_functions.csv_to_list(data_dir + r'\scotus',
                                         'consolidation.csv',
                                         1, 0)

# Instantiate a directed graph object, D
D = nx.DiGraph()

# Add our nodes to D
for row in node_data:
    # It is really easy to add arbitrary info about each node or edge. For example, here, I load each node with a
    # date, judges and citation_id attribute.
    case_number = int(row[0])
    month, day, year = ['', '', ''] if row[3] is '' else [int(element) for element in row[3].rsplit('/')]
    file_date = '' if month is '' else datetime.date(year=year, month=month, day=day)
    judges = row[4]
    citation_id = '' if row[5] is '' else int(row[5])
    reporter_number = row[6]

    is_clean = row[7] == 'TRUE'
    if is_clean:
        D.add_node(case_number,
                   date=file_date,
                   judges=judges,
                   citation_id=citation_id,
                   node_color='b' if file_date == ''
                   else 'y')  # ((2016-file_date.year)/500., 0, 1 - (2016-file_date.year)/500.))

# Add our edges to D
for row in edgelist_data:
    citer = row[0]
    cited = row[1]
    # Edges point from cited to citer -- so the node with the highest out degree represents the most cited decision
    D.add_edge(int(row[1]), int(row[0]), random_attribute='random_string')

###############################
# EXPLORE STUFF ABOUT OUR GRAPH
###############################
# print '10 HIGHEST DEGREES:', sorted(nx.degree(D).values(), reverse=True)[:10]  # Gives 10 highest degrees in D
# print '10 HIGHEST IN-DEGREES:', sorted(D.in_degree().values(), reverse=True)[:10]  # Gives 10 highest IN-degrees in D
#
# # sorted_node_indegree_tuples is a list of tuples of the form (node, in-degree) of all nodes in D
# sorted_node_indegree_tuples = sorted(D.in_degree_iter(), key=itemgetter(1), reverse=True)
# # sorted_node_outdegree_tuples is a list of tuples of the form (node, out-degree) of all nodes in D
# sorted_node_outdegree_tuples = sorted(D.out_degree_iter(), key=itemgetter(1), reverse=True)

############################
# VISUALIZE ASPECTS OF GRAPH
############################

# # Make a subgraph of the network
# S = D.copy()  # Create a copy of D
# # nodes_to_delete = [tup[0] for tup in sorted_node_outdegree_tuples[1000:]]  # Keep only 1000 highest out-degree nodes
# nodes_to_delete = []
# for node in nodes_to_delete:
#     S.remove_node(node)
# nx.draw(S, arrows=True, node_color='y')
# plt.show()
#
# # Make a out-degree rank plot of netowrk
# # degree sequence
# degree_sequence = sorted([tup[1] for tup in sorted(D.out_degree_iter(), reverse=True)], reverse=True)
# dmax = max(degree_sequence)
# plt.subplot(121)
# plt.loglog(degree_sequence, 'b-', marker='o')
# plt.title("Degree rank plot")
# plt.ylabel("in degree")
# plt.xlabel("rank")
#
# # Make a histogram of the out-degrees
# plt.subplot(122)
# data = degree_sequence
#
# # fixed bin size
# bins = np.arange(min(degree_sequence),
#                  max(degree_sequence),
#                  5)  # fixed bin size
# plt.xlim([min(data)-5, max(data)+5])
# plt.hist(data, bins=bins, alpha=0.5)
# plt.title('In degree histogram')
# plt.xlabel('variable X (bin size = 5)')
# plt.ylabel('count')
# plt.show()
