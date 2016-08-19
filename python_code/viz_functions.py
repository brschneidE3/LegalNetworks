from __future__ import division

__author__ = 'michael'

import networkx as nx
import matplotlib.pyplot as plt
import os
import datetime
from operator import itemgetter
import numpy as np
import calendar
import time
from collections import OrderedDict
import math
import json
import webbrowser

def years_useable(graph_object):
    '''
    prints out the range of years you can use for network visualization
    '''
    G = graph_object.copy()

    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] =='':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    print "years you should use: from " , min(years) , " to " , max(years)

def years_useable_after_del(graph_object):
    '''
    prints out the range of years you can use for network visualization, AFTER deleting zero-degree nodes
    '''
    G = graph_object.copy()

    solitary = [n for n,d in G.degree_iter() if d==0]
    G.remove_nodes_from(solitary)

    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] =='':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    print "after deleting nodes, years you should use: from " , min(years) , " to " , max(years)

def rank_plot_and_histogram(graph_object, deg_type, save_dir):
    '''
    USAGE: rank_plot_and_histogram(D, 'in_degree', 'some_directory/plot_test0.png')
    
    deg_type: (String)
        - 'in_degree'
        - 'out_degree'
        - 'degree'
    
    Note: degree = in_degree + out_degree
    '''
    
    fig = plt.figure()
    fig.set_size_inches(12,8)

    if deg_type == 'in_degree':
        ###################################
        # In-Degree Rank Plot and Histogram
        ###################################
        # Make an in-degree rank plot of network
        in_degree_sequence = sorted([tup[1] for tup in sorted(graph_object.in_degree_iter(), reverse=True)], reverse=True)  # in degree sequence
        in_dmax = max(in_degree_sequence)
        plt.subplot(121)
        plt.loglog(in_degree_sequence, 'b-', marker='o')
        plt.title("In-Degree Rank Plot")
        plt.ylabel("In-Degree")
        plt.xlabel("Rank")

        # Make a histogram of the in-degrees
        plt.subplot(122)
        in_data = in_degree_sequence
        # fixed bin size
        in_bins = np.arange(min(in_degree_sequence), max(in_degree_sequence), 5)  # fixed bin size
        plt.xlim([min(in_data)-5, max(in_data)+5])
        plt.hist(in_data, bins=in_bins, alpha=0.5)
        plt.title('In-Degree Histogram')
        plt.xlabel('In-Degree (Bin Size = 5)')
        plt.ylabel('Frequency')
        plt.savefig(save_dir)

    if deg_type == 'out_degree':
        ####################################
        # Out-Degree Rank Plot and Histogram
        ####################################
        # Make an out-degree rank plot of network
        out_degree_sequence = sorted([tup[1] for tup in sorted(graph_object.out_degree_iter(), reverse=True)], reverse=True)  # out degree sequence
        out_dmax = max(out_degree_sequence)
        plt.subplot(121)
        plt.loglog(out_degree_sequence, 'b-', marker='o', color='red')
        plt.title("Out-Degree Rank Plot")
        plt.ylabel("Out-Degree")
        plt.xlabel("Rank")

        # Make a histogram of the out-degrees
        plt.subplot(122)
        out_data = out_degree_sequence
        # fixed bin size
        out_bins = np.arange(min(out_degree_sequence), max(out_degree_sequence), 5)  # fixed bin size
        plt.xlim([min(out_data)-5, max(out_data)+5])
        plt.hist(out_data, bins=out_bins, alpha=0.5, color='red')
        plt.title('Out-Degree Histogram')
        plt.xlabel('Out-Degree (Bin Size = 5)')
        plt.ylabel('Frequency')
        plt.savefig(save_dir)

    if deg_type == 'degree':
        ################################
        # Degree Rank Plot and Histogram
        ################################
        # Make a degree rank plot of network
        degree_sequence = sorted([tup[1] for tup in sorted(graph_object.degree_iter(), reverse=True)], reverse=True)  # degree sequence
        dmax = max(degree_sequence)
        plt.subplot(121)
        plt.loglog(degree_sequence, 'b-', marker='o', color = 'purple')
        plt.title("Degree Rank Plot")
        plt.ylabel("Degree")
        plt.xlabel("Rank")

        # Make a histogram of the out-degrees
        plt.subplot(122)
        data = degree_sequence
        # fixed bin size
        bins = np.arange(min(degree_sequence), max(degree_sequence), 5)  # fixed bin size
        plt.xlim([min(data)-5, max(data)+5])
        plt.hist(data, bins=bins, alpha=0.5, color='purple')
        plt.title('Degree Histogram')
        plt.xlabel('Degree (Bin Size = 5)')
        plt.ylabel('Histogram')
        plt.savefig(save_dir)

def rank_plot_and_histogram_given_years(graph_object, start_year, end_year, deg_type, save_dir):
    '''
    USAGE: rank_plot_and_histogram(D, 'in_degree', 1980, 1989, 'some_directory/plot_test0.png')
    
    start_year, end_year (Int):
        - Use any subset from 'years_useable(graph_object)'
    
    deg_type: (String)
        - 'in_degree'
        - 'out_degree'
        - 'degree'
    
    Note: degree = in_degree + out_degree
    '''
    
    ##################################################################
    # Make Graph G which has nodes and edges only from specified years
    ##################################################################
    G = graph_object.copy()
    
    nodes_to_delete = []
    for each_node in G.nodes():
        if not (start_year <= G.node[each_node]['year'] <= end_year):
            nodes_to_delete.append(each_node)
    
    G.remove_nodes_from(nodes_to_delete)
    
    fig = plt.figure()
    fig.set_size_inches(12,8)
    
    if deg_type == 'in_degree':
        ###################################
        # In-Degree Rank Plot and Histogram
        ###################################
        # Make an in-degree rank plot of network
        nodes_G = G.nodes()
        in_degrees_G = graph_object.in_degree() # keep original in_degree information
        indeg_iter_list = [in_degrees_G[n] for n in nodes_G]
        in_degree_sequence = sorted(indeg_iter_list, reverse=True)
        in_dmax = max(in_degree_sequence)
        plt.subplot(121)
        plt.loglog(in_degree_sequence, 'b-', marker='o')
        plt.title("In-Degree Rank Plot from " +  str(start_year) + " to " + str(end_year))
        plt.ylabel("In-Degree")
        plt.xlabel("Rank")

        # Make a histogram of the in-degrees
        plt.subplot(122)
        in_data = in_degree_sequence
        # fixed bin size
        in_bins = np.arange(min(in_degree_sequence), max(in_degree_sequence), 5)  # fixed bin size
        plt.xlim([min(in_data)-5, max(in_data)+5])
        plt.hist(in_data, bins=in_bins, alpha=0.5)
        plt.title("In-Degree Histogram from " + str(start_year) + " to " + str(end_year))
        plt.xlabel('In-Degree (Bin Size = 5)')
        plt.ylabel('Frequency')
        plt.savefig(save_dir)

    if deg_type == 'out_degree':
        ####################################
        # Out-Degree Rank Plot and Histogram
        ####################################
        # Make an out-degree rank plot of network
        nodes_G = G.nodes()
        out_degrees_G = graph_object.out_degree() # keep original out_degree information
        outdeg_iter_list = [out_degrees_G[n] for n in nodes_G]
        out_degree_sequence = sorted(outdeg_iter_list, reverse=True)
        out_dmax = max(out_degree_sequence)
        plt.subplot(121)
        plt.loglog(out_degree_sequence, 'b-', marker='o', color='red')
        plt.title("Out-Degree Rank Plot from " + str(start_year) + " to " + str(end_year))
        plt.ylabel("Out-Degree")
        plt.xlabel("Rank")

        # Make a histogram of the out-degrees
        plt.subplot(122)
        out_data = out_degree_sequence
        # fixed bin size
        out_bins = np.arange(min(out_degree_sequence), max(out_degree_sequence), 5)  # fixed bin size
        plt.xlim([min(out_data)-5, max(out_data)+5])
        plt.hist(out_data, bins=out_bins, alpha=0.5, color='red')
        plt.title('Out-Degree Histogram from ' + str(start_year) + ' to ' + str(end_year))
        plt.xlabel('Out-Degree (Bin Size = 5)')
        plt.ylabel('Frequency')
        plt.savefig(save_dir)

    if deg_type == 'degree':
        ################################
        # Degree Rank Plot and Histogram
        ################################
        # Make a degree rank plot of network
        nodes_G = G.nodes()
        degrees_G = graph_object.degree() # keep original degree information
        deg_iter_list = [degrees_G[n] for n in nodes_G]
        degree_sequence = sorted(deg_iter_list, reverse=True)
        dmax = max(degree_sequence)
        plt.subplot(121)
        plt.loglog(degree_sequence, 'b-', marker='o', color = 'purple')
        plt.title("Degree Rank Plot from " + str(start_year) + " to " + str(end_year))
        plt.ylabel("Degree")
        plt.xlabel("Rank")

        # Make a histogram of the out-degrees
        plt.subplot(122)
        data = degree_sequence
        # fixed bin size
        bins = np.arange(min(degree_sequence), max(degree_sequence), 5)  # fixed bin size
        plt.xlim([min(data)-5, max(data)+5])
        plt.hist(data, bins=bins, alpha=0.5, color='purple')
        plt.title('Degree Histogram ' + str(start_year) + ' to ' + str(end_year))
        plt.xlabel('Degree (Bin Size = 5)')
        plt.ylabel('Histogram')
        plt.savefig(save_dir)

def spring_layout(graph_object, start_year, end_year, deg_type, del_zero_deg_nodes, save_dir):
    '''
    USAGE: spring_layout(D, 1980, 1989, 'in_degree', False, 'some_directory/plot_test.png')

    NOTE: graph_object should contain 'year' attribute for each node; If not, simply make one from 'date' attribute
        - If no 'year' attribute, your graph_object can't use this function

    NOTE: TAKES (MUCH) LONGER FOR BIGGER NETWORKS, compared to chronological_layout

    start_year, end_year (Int):
        - Use any subset either from 'years_useable(graph_object)' or 'years_useable_after_del(graph_object)'

    deg_type: (String)
        - 'in_degree'
        - 'out_degree'
        - 'degree' (in_degree + out_degree)

    del_zero_deg_nodes: (Boolean)
        - True (delete all the nodes with zero degree, while keeping the original degree information of remaining nodes)
        - False (don't delete all the nodes with zero degree)

    '''

    start_time = time.time() # start timer to approximate how long this function takes

    ###############
    # Make Graph G
    ###############
    G = graph_object.copy()

    if del_zero_deg_nodes:
        solitary = [n for n,d in G.degree_iter() if d==0]
        G.remove_nodes_from(solitary)

    nodes_to_delete = []
    for each_node in G.nodes():
        if not (start_year <= G.node[each_node]['year'] <= end_year):
            nodes_to_delete.append(each_node)

    # Remove nodes that aren't contained (inclusively) between 'start_year' and 'end_year' you want to analyze:
    G.remove_nodes_from(nodes_to_delete)

    #Get Year Attribute for G.nodes()
    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] =='':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    # Get Title
    if del_zero_deg_nodes:
        title = str(min(years)) + '-' + str(max(years)) + ' SCOTUS Network with ' + str(G.number_of_nodes()) + ' Nodes After Deleting Zero-Degree Nodes in the Entire Network ' + '(colored nodes by ' + deg_type + ')'
    else:
        title = str(min(years)) + '-' + str(max(years)) + ' SCOTUS Network with ' + str(G.number_of_nodes()) + ' Nodes ' + '(colored nodes by ' + deg_type + ')'

    ####################################################################################
    # Draw Network with Spring Layout (Default) and Colored Nodes by In/Out/Total-Degree
    ####################################################################################

    # set figure size, set figure title
    fig = plt.figure()
    fig.set_size_inches(30, 30)
    fig.suptitle(title, fontsize=30)

    # for coloring the nodes by in_degree/out_degree/degree
    nodes_G = G.nodes() ## list of nodes
    if (deg_type == 'in_degree'):
        # In-Degree of ech node in a list (for coloring the nodes by in-degree later using cmap=plt.cm.Blues)
        in_degrees_G = graph_object.in_degree() ## dict of key (node) : value (in-degree) ; keep original in_degree information
        n_color_G = np.asarray([in_degrees_G[n] for n in nodes_G]) ## list of node's respective in-degrees
    if (deg_type == 'out_degree'):
        # Out-Degree of each node in a list (for coloring the nodes by out-degree later using cmap=plt.cm.Blues)
        out_degrees_G = graph_object.out_degree() ## dict of key(node): value(out-degree) ; keep original out_degree information
        n_color_G = np.asarray([out_degrees_G[n] for n in nodes_G]) ## list of node's respective out-degrees
    if (deg_type == 'degree'):
        # Degree of each node in a list (for coloring the nodes by degree later using cmap=plt.cm.Blues)
        degrees_G = graph_object.degree() ## dict of key(node): value(degree) ; keep original degree information
        n_color_G = np.asarray([degrees_G[n] for n in nodes_G]) ## list of node's respective degrees

    # draw network
    pos_G = nx.spring_layout(G)
    nx.draw(G, pos=pos_G, node_size = 30, arrows=True, with_labels=False, node_color=n_color_G, cmap=plt.cm.Blues, edge_color='black', width=1.0/10, style='solid')
    plt.savefig(save_dir)

    print("--- %s seconds ---" % (time.time() - start_time)) # end timer to approximate how long it takes to plot/draw the network

def chronological_layout(graph_object, start_year, end_year, deg_type, del_zero_deg_nodes, save_dir):
    '''
    USAGE: chronological_layout(D, 1980, 1989, 'in_degree', False, 'some_directory/plot_test.png')

    NOTE: graph_object should contain 'year' attribute for each node; If not, simply make one from 'date' attribute
        - If no 'year' attribute, your graph_object can't use this function

    start_year, end_year (Int):
        - Use any subset either from 'years_useable(graph_object)' or 'years_useable_after_del(graph_object)'

    deg_type: (String)
        - 'in_degree'
        - 'out_degree'
        - 'degree'

    del_zero_deg_nodes: (Boolean)
        - True (delete all the nodes with zero degree, while keeping the original degree information of remaining nodes)
        - False (don't delete all the nodes with zero degree)
    '''
    
    start_time = time.time() # start timer to approximate how long this function takes

    ###############
    # Make Graph G
    ###############
    G = graph_object.copy()

    if del_zero_deg_nodes:
        solitary = [n for n,d in G.degree_iter() if d==0]
        G.remove_nodes_from(solitary)

    nodes_to_delete = []
    for each_node in G.nodes():
        if not (start_year <= G.node[each_node]['year'] <= end_year):
            nodes_to_delete.append(each_node)

    G.remove_nodes_from(nodes_to_delete)

    # Get Year Attribute for G.nodes()
    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    # Get Date Attribute for G.nodes()
    dates = []
    cases_without_dates = []
    for each_node in G.nodes():
        if G.node[each_node]['date'] == '':
            cases_without_dates.append(each_node)
        else:
            dates.append(G.node[each_node]['date'])

    #Get Title
    if del_zero_deg_nodes:
        title = str(min(years)) + '-' + str(max(years)) + ' SCOTUS Network with ' + str(G.number_of_nodes()) + ' Nodes After Deleting Zero-Degree Nodes in the Entire Network ' + '(colored nodes by ' + deg_type + ')'
    else:
        title = str(min(years)) + '-' + str(max(years)) + ' SCOTUS Network with ' + str(G.number_of_nodes()) + ' Nodes ' + '(colored nodes by ' + deg_type + ')'

    ###########################################
    # For Coloring by In/Out/Total-Degree Later
    ###########################################
    nodes_G = G.nodes()
    if deg_type == 'in_degree':
        # In-Degree of each node in a list (for coloring the nodes by in-degree later using cmap=plt.cm.Blues)
        in_degrees_G = graph_object.in_degree() # keep original in_degree information
        n_color_G = np.asarray([in_degrees_G[n] for n in nodes_G]) ## list of node's respective in-degrees
    if deg_type == 'out_degree':
        # Out-Degree of each node in a list (for coloring the nodes by out-degree later using cmap=plt.cm.Blues)
        out_degrees_G = graph_object.out_degree() # keep original out_degree information
        n_color_G = np.asarray([out_degrees_G[n] for n in nodes_G]) ## list of node's respective out-degrees
    if deg_type == 'degree':
        # Degrees of each node in a list (for coloring the nodes by degree later using cmap=plt.cm.Blues)
        degrees_G = graph_object.degree() # keep original degree information
        n_color_G = np.asarray([degrees_G[n] for n in nodes_G]) ## list of node's respective degrees

    ####################################################
    # Get X- and Y- Coordinates for Chronological Layout
    ####################################################
    ### X-Coordinates for each node in network:

    # X-Coordinates are YEAR VALUES (i.e. 1986 June 16th = 1989.458333...)
    X_G = []
    for specific_date in dates:
        temp_day = specific_date.day
        temp_month = specific_date.month
        temp_year = specific_date.year
        total_months = 12
        if temp_month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
            total_days = 31
        elif temp_month == 4 or 6 or 9 or 11:
            total_days = 30
        else: #temp_month = 2
            if calendar.isleap(temp_year):
                total_days = 29
            else: # it isn't leap year
                total_days = 28
        date_to_int = temp_year + (temp_month-1)/total_months + (temp_day-1)/(total_months * total_days)
        X_G.append(date_to_int)

    ### Y-Coordinates for each node in network:

    # Y-Coordinates are the respective in-degree/out-degree/degree of each node:
    Y_G = n_color_G

    ### make list of tuples of (x,y) coordinates for respective nodes: [(x1,y1), (x2,y2), ... , (xn,yn)]:
    list_of_tuples_G = zip(X_G, Y_G)

    #################################################################################
    # Draw Network with Chronological Layout and Colored Nodes by In/Out/Total-Degree
    #################################################################################
    '''
    Note: Ill-Advised to Change Around sizes/scaling/margins/etc. of plot, unless otherwise stated
    '''

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50, 30)
    fig.suptitle(title, fontsize=50)

    # draw network
    pre_pos_G = dict(zip(G.nodes(), list_of_tuples_G)) # make a dictionary and assign each node its coordinate point
    pos_G = nx.spring_layout(G, fixed = G.nodes(), pos = pre_pos_G) # you have to fix the nodes in place!
    nx.draw_networkx(G, pos = pos_G, node_size=50, arrows=False, with_labels=False, node_color=n_color_G, cmap=plt.cm.Blues, edge_color='black', width=1.0/10, style='solid')
    '''
    Note: you can...
        1. turn on arrows (although not really necessary, since you know nodes at right are citing the nodes at left)
        2. change the coloring of nodes--i.e. cmap = plt.cm.Reds
    * Other characteristics are optimized for visualization purposes in the author's humble opinion, but feel free to change for experimentation
    '''

    # add xlabel, remove ylabel, set x-margin, set y-margin, set x-ticks
    plt.xlabel("time", fontsize=50)
    plt.ylabel(deg_type, fontsize=50)
    axes = plt.gca()
    axes.set_xlim([min(years), max(years)+1])
    axes.set_ylim([min(Y_G)-1, max(Y_G)+1])
    plt.savefig(save_dir)

    print("--- %s seconds ---" % (time.time() - start_time)) # end timer to approximate how long it takes to plot/draw the network

def indeg_time_series_plot(graph_object, mean_bool, median_bool, total_cases_bool, save_dir):
    '''
    USAGE: indeg_time_series_plot(D, True, True, True, 'some_directory/plot_test.png')
    '''
    
    start_time = time.time() # start timer to approximate how long this function takes

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50,30)
    fig.suptitle("Entire SCOTUS Network (In-Degree Information)", fontsize=35)

    #####################################################
    # In-Degree Information (Mean or Median) of Each Year
    #####################################################
    G = graph_object.copy()

    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    sorted_years = list(set(years))

    # Remove the nodes with empty year attributes
    G.remove_nodes_from(cases_without_years)    

    nodes_G = G.nodes() ## list of nodes
    in_degrees_G = graph_object.in_degree() ## dict of key (node) : value (in-degree) ; keep original in_degree information
    n_color_G = [in_degrees_G[n] for n in nodes_G] ## list of nodes's respective in-degrees

    year_indeg = zip(years, n_color_G) ## make list of tuples [(year_1, indeg_1), (year_2, indeg_2), ... , (year_n, indeg_n)]
    sorted_by_year = sorted(year_indeg, key=itemgetter(0)) ## sort the above tuples by year in increasing order

    # average in-degree in each year, median in-degree in each year
    year_indeg_dict = OrderedDict() ## get a dictionary of { {year : [all the in_degrees within that year]} , ... , {year: ... } }
    for each_tuple in sorted_by_year:
        if not year_indeg_dict.has_key(each_tuple[0]):
            year_indeg_dict[each_tuple[0]] = []
        year_indeg_dict[each_tuple[0]].append(each_tuple[1])

    in_degrees_mean_list = [] ## get the respective mean of in-degrees for each year
    in_degrees_median_list = [] ## get the respective median of in-degrees for each year
    for value in year_indeg_dict.itervalues():
        some_mean = sum(value)/len(value)
        in_degrees_mean_list.append(some_mean)
        some_median = np.median(np.array(value))
        in_degrees_median_list.append(some_median)

    # total cases count in each year:
    total_cases_list = []
    for value in year_indeg_dict.itervalues():
        total_cases_list.append(len(value))    

    # scale down the total_cases by 500 for visualization optimization
    scaled_total_cases_list = [x/500 for x in total_cases_list]    

    # Plot:
    if (mean_bool==True) and (median_bool==False) and (total_cases_bool==False):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.legend(["Mean In-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, in_degrees_median_list)
        plt.legend(["Mean In-Degree of Each Year", "Median In-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean In-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, in_degrees_median_list)
        plt.legend(["Median In-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, in_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Median In-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, total_cases_list)
        plt.legend(["Total Cases of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, in_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean In-Degree of Each Year", "Median In-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)
    else: ## (mean_bool==False) and (median_bool==False) and (total_cases_bool==False):
        print "Printing Everything Instead..."
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, in_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean In-Degree of Each Year", "Median In-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)

    plt.xlabel('Years', fontsize=30)
    axes=plt.gca()
    axes.set_xlim([min(sorted_years), max(sorted_years)])
    plt.xticks(np.arange(min(sorted_years), max(sorted_years)+1, 5))
    plt.savefig(save_dir)

    #end timer
    print("--- %s seconds ---" % (time.time() - start_time))

def outdeg_time_series_plot(graph_object, mean_bool, median_bool, total_cases_bool, save_dir):
    '''
    USAGE: outdeg_time_series_plot(D, True, True, True, 'some_directory/plot_test.png')
    '''
    
    start_time = time.time() # start timer to approximate how long this function takes

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50,30)
    fig.suptitle("Entire SCOTUS Network (Out-Degree Information)", fontsize=35)

    ######################################################
    # Out-Degree Information (Mean or Median) of Each Year
    ######################################################
    G = graph_object.copy()

    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    sorted_years = list(set(years))

    # Remove the nodes with empty year attributes
    G.remove_nodes_from(cases_without_years)    

    nodes_G = G.nodes() ## list of nodes
    out_degrees_G = graph_object.out_degree() ## dict of key (node) : value (out-degree) ; keep original out_degree information
    n_color_G = [out_degrees_G[n] for n in nodes_G] ## list of nodes's respective out-degrees

    year_outdeg = zip(years, n_color_G) ## make list of tuples [(year_1, outdeg_1), (year_2, outdeg_2), ... , (year_n, outdeg_n)]
    sorted_by_year = sorted(year_outdeg, key=itemgetter(0)) ## sort the above tuples by year in increasing order

    # average out-degree in each year, median out-degree in each year
    year_outdeg_dict = OrderedDict() ## get a dictionary of { {year : [all the out_degrees within that year]} , ... , {year: ... } }
    for each_tuple in sorted_by_year:
        if not year_outdeg_dict.has_key(each_tuple[0]):
            year_outdeg_dict[each_tuple[0]] = []
        year_outdeg_dict[each_tuple[0]].append(each_tuple[1])

    out_degrees_mean_list = [] ## get the respective mean of out-degrees for each year
    out_degrees_median_list = [] ## get the respective median of out-degrees for each year
    for value in year_outdeg_dict.itervalues():
        some_mean = sum(value)/len(value)
        out_degrees_mean_list.append(some_mean)
        some_median = np.median(np.array(value))
        out_degrees_median_list.append(some_median)

    # total cases count in each year:
    total_cases_list = []
    for value in year_outdeg_dict.itervalues():
        total_cases_list.append(len(value))    

    # scale down the total_cases by 500 for visualization optimization
    scaled_total_cases_list = [x/500 for x in total_cases_list]    

    # Plot:
    if (mean_bool==True) and (median_bool==False) and (total_cases_bool==False):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.legend(["Mean Out-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, out_degrees_median_list)
        plt.legend(["Mean Out-Degree of Each Year", "Median Out-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean Out-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, out_degrees_median_list)
        plt.legend(["Median Out-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, out_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Median Out-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, total_cases_list)
        plt.legend(["Total Cases of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, out_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean Out-Degree of Each Year", "Median Out-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)
    else: ## (mean_bool==False) and (median_bool==False) and (total_cases_bool==False):
        print "Printing Everything Instead..."
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, out_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean Out-Degree of Each Year", "Median Out-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)

    plt.xlabel('Years', fontsize=30)
    axes=plt.gca()
    axes.set_xlim([min(sorted_years), max(sorted_years)])
    plt.xticks(np.arange(min(sorted_years), max(sorted_years)+1, 5))
    plt.savefig(save_dir)

    # end timer
    print("--- %s seconds ---" % (time.time() - start_time))

def indeg_time_series_plot_after_del(graph_object, mean_bool, median_bool, total_cases_bool, save_dir):
    '''
    USAGE: indeg_time_series_plot_after_deletion(D, True, True, True, 'some_directory/plot_test.png')
    '''
    
    start_time = time.time() # start timer to approximate how long this function takes

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50,30)
    fig.suptitle("Entire SCOTUS Network After Deleting Zero-Degree Nodes (In-Degree Information)", fontsize=35)

    ######################################################################################
    # In-Degree Information (Mean or Median) of Each Year After Deleting Zero-Degree Nodes
    ######################################################################################
    G = graph_object.copy()

    # remove nodes with zero degree
    solitary = [n for n,d in G.degree_iter() if d==0]
    G.remove_nodes_from(solitary)

    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    sorted_years = list(set(years))

    # Remove the nodes with empty year attributes
    G.remove_nodes_from(cases_without_years)    

    nodes_G = G.nodes() ## list of nodes
    in_degrees_G = graph_object.in_degree() ## dict of key (node) : value (in-degree) ; keep original in_degree information
    n_color_G = [in_degrees_G[n] for n in nodes_G] ## list of nodes's respective in-degrees

    year_indeg = zip(years, n_color_G) ## make list of tuples [(year_1, indeg_1), (year_2, indeg_2), ... , (year_n, indeg_n)]
    sorted_by_year = sorted(year_indeg, key=itemgetter(0)) ## sort the above tuples by year in increasing order

    # average in-degree in each year, median in-degree in each year
    year_indeg_dict = OrderedDict() ## get a dictionary of { {year : [all the in_degrees within that year]} , ... , {year: ... } }
    for each_tuple in sorted_by_year:
        if not year_indeg_dict.has_key(each_tuple[0]):
            year_indeg_dict[each_tuple[0]] = []
        year_indeg_dict[each_tuple[0]].append(each_tuple[1])

    in_degrees_mean_list = [] ## get the respective mean of in-degrees for each year
    in_degrees_median_list = [] ## get the respective median of in-degrees for each year
    for value in year_indeg_dict.itervalues():
        some_mean = sum(value)/len(value)
        in_degrees_mean_list.append(some_mean)
        some_median = np.median(np.array(value))
        in_degrees_median_list.append(some_median)

    # total cases count in each year:
    total_cases_list = []
    for value in year_indeg_dict.itervalues():
        total_cases_list.append(len(value))    

    # scale down the total_cases by 15 for visualization optimization
    scaled_total_cases_list = [x/15 for x in total_cases_list]    

    # Plot:
    if (mean_bool==True) and (median_bool==False) and (total_cases_bool==False):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.legend(["Mean In-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, in_degrees_median_list)
        plt.legend(["Mean In-Degree of Each Year", "Median In-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean In-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, in_degrees_median_list)
        plt.legend(["Median In-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, in_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Median In-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, total_cases_list)
        plt.legend(["Total Cases of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, in_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean In-Degree of Each Year", "Median In-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)
    else: ## (mean_bool==False) and (median_bool==False) and (total_cases_bool==False):
        print "Printing Everything Instead..."
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, in_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean In-Degree of Each Year", "Median In-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)

    plt.xlabel('Years', fontsize=30)
    axes=plt.gca()
    axes.set_xlim([min(sorted_years), max(sorted_years)])
    plt.xticks(np.arange(min(sorted_years), max(sorted_years)+1, 5))
    plt.savefig(save_dir)

    # end timer
    print("--- %s seconds ---" % (time.time() - start_time))

def outdeg_time_series_plot_after_del(graph_object, mean_bool, median_bool, total_cases_bool, save_dir):
    '''
    USAGE: outdeg_time_series_plot_after_deletion(D, True, True, True, 'some_directory/plot_test.png')
    '''
    
    start_time = time.time() # start timer to approximate how long this function takes

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50,30)
    fig.suptitle("Entire SCOTUS Network After Deleting Zero-Degree Nodes (Out-Degree Information)", fontsize=35)

    ######################################################################################
    # Out-Degree Information (Mean or Median) of Each Year After Deleting Zero-Degree Nodes
    ######################################################################################
    G = graph_object.copy()

    # remove nodes with zero degree
    solitary = [n for n,d in G.degree_iter() if d==0]
    G.remove_nodes_from(solitary)

    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    sorted_years = list(set(years))

    # Remove the nodes with empty year attributes
    G.remove_nodes_from(cases_without_years)    

    nodes_G = G.nodes() ## list of nodes
    out_degrees_G = graph_object.out_degree() ## dict of key (node) : value (out-degree) ; keep original out_degree information
    n_color_G = [out_degrees_G[n] for n in nodes_G] ## list of nodes's respective out-degrees

    year_outdeg = zip(years, n_color_G) ## make list of tuples [(year_1, outdeg_1), (year_2, outdeg_2), ... , (year_n, outdeg_n)]
    sorted_by_year = sorted(year_outdeg, key=itemgetter(0)) ## sort the above tuples by year in increasing order

    # average out-degree in each year, median out-degree in each year
    year_outdeg_dict = OrderedDict() ## get a dictionary of { {year : [all the out_degrees within that year]} , ... , {year: ... } }
    for each_tuple in sorted_by_year:
        if not year_outdeg_dict.has_key(each_tuple[0]):
            year_outdeg_dict[each_tuple[0]] = []
        year_outdeg_dict[each_tuple[0]].append(each_tuple[1])

    out_degrees_mean_list = [] ## get the respective mean of out-degrees for each year
    out_degrees_median_list = [] ## get the respective median of out-degrees for each year
    for value in year_outdeg_dict.itervalues():
        some_mean = sum(value)/len(value)
        out_degrees_mean_list.append(some_mean)
        some_median = np.median(np.array(value))
        out_degrees_median_list.append(some_median)

    # total cases count in each year:
    total_cases_list = []
    for value in year_outdeg_dict.itervalues():
        total_cases_list.append(len(value))    

    # scale down the total_cases by 15 for visualization optimization
    scaled_total_cases_list = [x/15 for x in total_cases_list]    

    # Plot:
    if (mean_bool==True) and (median_bool==False) and (total_cases_bool==False):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.legend(["Mean Out-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, out_degrees_median_list)
        plt.legend(["Mean Out-Degree of Each Year", "Median Out-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean Out-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, out_degrees_median_list)
        plt.legend(["Median Out-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, out_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Median Out-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, total_cases_list)
        plt.legend(["Total Cases of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, out_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean Out-Degree of Each Year", "Median Out-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)
    else: ## (mean_bool==False) and (median_bool==False) and (total_cases_bool==False):
        print "Printing Everything Instead..."
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, out_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean Out-Degree of Each Year", "Median Out-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)

    plt.xlabel('Years', fontsize=30)
    axes=plt.gca()
    axes.set_xlim([min(sorted_years), max(sorted_years)])
    plt.xticks(np.arange(min(sorted_years), max(sorted_years)+1, 5))
    plt.savefig(save_dir)

    # end timer
    print("--- %s seconds ---" % (time.time() - start_time))

def total_vs_zero_cases(graph_object, save_dir):
    start_time = time.time() # start timer to approximate how long this function takes

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50,30)
    fig.suptitle("Number of Zero-Degree Cases vs. Total Number of Cases of Each Year in Entire SCOTUS Network", fontsize=35)
    #################################################################
    # Total Number of Cases vs. Number of Zero-Degree Cases Each Year
    #################################################################
    G = graph_object.copy()
    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    sorted_years = list(set(years))

    # Remove the nodes without empty year attributes
    G.remove_nodes_from(cases_without_years)

    nodes_G = G.nodes() ## list of nodes
    degrees_G = graph_object.degree() ## dict of key (node) : value (degree) ; keep original degree information
    n_color_G = [degrees_G[n] for n in nodes_G] ## list of nodes's respective degrees

    year_deg = zip(years, n_color_G) ## get list of tuples, where each tuple is (node_year, node_degree)
    sorted_by_year = sorted(year_deg, key=itemgetter(0)) ## sort the list of tuples by year in increasing order

    # zero degree cases count in each year:
    year_deg_dict = OrderedDict()
    for each_tuple in sorted_by_year:
        if not year_deg_dict.has_key(each_tuple[0]):
            year_deg_dict[each_tuple[0]] = []
        if each_tuple[1] == 0:
            year_deg_dict[each_tuple[0]].append(each_tuple[1])

    zero_deg_count_list = []
    for value in year_deg_dict.itervalues():
        zero_deg_count_list.append(len(value))

    # total cases count in each year:
    year_deg_dict2 = OrderedDict()
    for each_tuple in sorted_by_year:
        if not year_deg_dict2.has_key(each_tuple[0]):
            year_deg_dict2[each_tuple[0]] = []
        year_deg_dict2[each_tuple[0]].append(each_tuple[1])

    total_cases_list = []
    for value in year_deg_dict2.itervalues():
        total_cases_list.append(len(value))

    # Plot:
    plt.plot(sorted_years, zero_deg_count_list) # zero degrees plot
    plt.plot(sorted_years, total_cases_list) # total cases plot
    plt.legend(['No. of Zero Degree Cases/Year','Total No. of Cases/Year'],loc='upper left', fontsize=35)
    plt.xlabel('Years', fontsize=30)
    plt.ylabel('Number of Cases', fontsize=30)
    axes=plt.gca()
    axes.set_xlim([min(sorted_years), max(sorted_years)])
    plt.xticks(np.arange(min(sorted_years), max(sorted_years)+1, 5))
    plt.savefig(save_dir)
    plt.show()

    # end timer
    print("--- %s seconds ---" % (time.time() - start_time))

def bigball_time_layout(graph_object, start_year, end_year, deg_type, info_type, del_zero_deg_nodes, save_dir):

    '''
    USAGE: bigball_time_layout(D, 1980, 1989, 'in_degree', 'mean', False, 'some_directory/plot_test.png')

    NOTE: graph_object should contain 'year' attribute for each node; If not, simply make one from 'date' attribute
        - If no 'year' attribute, your graph_object can't use this function

    start_year, end_year (Int):
        - Use any subset either from 'years_useable(graph_object)' or 'years_useable_after_del(graph_object)'

    deg_type: (String)
        - 'in_degree'
        - 'out_degree'
        - 'degree'

    info_type: (String)
        - 'mean'
        - 'median'
        - 'total'

    del_zero_deg_nodes: (Boolean)
        - True (delete all the nodes with zero degree, while keeping the original degree information of remaining nodes)
        - False (don't delete all the nodes with zero degree)
    '''

    start_time = time.time() # start timer to approximate how long this function takes

    ###############
    # Make Graph G
    ###############
    G = graph_object.copy()

    if del_zero_deg_nodes:
        solitary = [n for n,d in G.degree_iter() if d==0]
        G.remove_nodes_from(solitary)
    
    nodes_to_delete = []
    for each_node in G.nodes():
        if not (start_year <= G.node[each_node]['year'] <= end_year):
            nodes_to_delete.append(each_node)

    G.remove_nodes_from(nodes_to_delete)

    # Get Year Attribute for G.nodes()
    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    # Get Date Attribute for G.nodes()
    dates = []
    cases_without_dates = []
    for each_node in G.nodes():
        if G.node[each_node]['date'] == '':
            cases_without_dates.append(each_node)
        else:
            dates.append(G.node[each_node]['date'])

    # Get node, year information
    nodes_G = G.nodes() ## list of nodes
    year_nodes_tup = zip(years, nodes_G) ## make list of tuples [(year1, node1), ... , (year_n, node_n)]
    year_nodes_tup_sorted = sorted(year_nodes_tup, key=itemgetter(0)) ## sort the above tuples by year in increasing order

    # Turn above information into ordered dictionary
    year_nodes_dict = OrderedDict() ## get a dictionary of { {year: [all the nodes within that year]} , ... , {year: ...} }
    for each_tuple in year_nodes_tup_sorted:
        if not year_nodes_dict.has_key(each_tuple[0]):
            year_nodes_dict[each_tuple[0]] = []
        year_nodes_dict[each_tuple[0]].append(each_tuple[1])
    
    # Big Ball Layout where nodes represent the unique years
    G2 = G.copy()
    for year, list_of_nodes in year_nodes_dict.iteritems():
        G2.add_node(year,
                    num_of_nodes = len(list_of_nodes)
                    )
        for n1, n2, data in G2.edges(data=True):
            if n1 in list_of_nodes:
                G2.add_edge(year, n2, data)
            elif n2 in list_of_nodes:
                G2.add_edge(n1, year, data)

        G2.remove_nodes_from(list_of_nodes)

    #Get Title for Big Ball Layout
    if del_zero_deg_nodes:
        title = str(min(years)) + '-' + str(max(years)) + ' SCOTUS Network with ' + str(G2.number_of_nodes()) + ' Years After Deleting Zero-Degree Nodes in the Entire Network ' + '(colored nodes by ' + info_type + ' ' + deg_type + ')'
    else:
        title = str(min(years)) + '-' + str(max(years)) + ' SCOTUS Network with ' + str(G2.number_of_nodes()) + ' Years ' + '(colored nodes by ' + info_type + ' ' + deg_type + ')'

    # Get node_sizes for drawing the newtork later, which is based on the number of nodes/cases in a year
    node_sizes = []
    for each_node in G2.nodes():
        some_node_size = (G2.node[each_node]['num_of_nodes'])*5 # multiply by 5 for visualization purposes of node sizes
        node_sizes.append(some_node_size)
    
    # Get node, in/out-degree information
    if deg_type == 'in_degree':
        deg_dict = graph_object.in_degree() ## dict of key(node): value(in-degree) in original graph object
    if deg_type == 'out_degree':
        deg_dict = graph_object.out_degree() ## dict of key(node): value(out-degree) in original graph object
    if deg_type == 'degree':
        deg_dict = graph_object.degree() ## dict of key(node): value(degree) in original graph object
    deg_list = [deg_dict[n] for n in nodes_G] ## list of nodes' respective in/out/total-degrees in original graph object
    year_deg_tup = zip(years, deg_list) ## make list of tuples [(year1, in/out/total-deg1) , ... , (year_n, in/out/total-deg_n)] (original graph object)
    year_deg_tup_sorted = sorted(year_deg_tup, key=itemgetter(0)) ## sort the above tuples by year in increasing order (original graph object)

    # Turn above information into ordered dictionary
    year_deg_dict = OrderedDict() ## get a dictionary of { {year: [all the in/out/total_degrees within that year]} , ... , {year: ...} }
    for each_tuple in year_deg_tup_sorted:
        if not year_deg_dict.has_key(each_tuple[0]):
            year_deg_dict[each_tuple[0]] = []
        year_deg_dict[each_tuple[0]].append(each_tuple[1])

    if info_type == 'mean':
        # Get node colors for drawing the network later, which is based on the mean in/out/total-degree of that year
        node_colors = [] ## get the respective mean in/out/total-degree for each year
        for each_year in G2.nodes():
            degs = year_deg_dict[each_year]
            degs_mean = sum(degs)/len(degs)
            node_colors.append(degs_mean)

    if info_type == 'median':
        # Get node colors for drawing the network later, which is based on the median in/out/total-degree of that year
        node_colors = [] ## get the respective mean in/out/total-degree for each year
        for each_year in G2.nodes():
            degs = year_deg_dict[each_year]
            degs_median = np.median(np.array(degs))
            node_colors.append(degs_median)

    if info_type == 'total':
        # Get node colors for drawing the network later, which is based on the total in/out/total-degree of that year
        node_colors = [] ## get the respective mean in/out/total-degree for each year
        for each_year in G2.nodes():
            degs = year_deg_dict[each_year]
            degs_total = sum(degs)
            node_colors.append(degs_total)

    ###############################################
    # Get X- and Y- Coordinates for Big-Ball Layout
    ###############################################
    # X-Coordinates are the years
    X_G2 = G2.nodes()
    # Y-Coordinates are the mean/median/total in/out/total-degrees of that year
    Y_G2 = node_colors
    # make list of tuples of (x,y) coordinates for respective nodes: [(x1,y1), (x2,y2), ... , (xn,yn)]:
    coordinates_G2 = zip(X_G2, Y_G2)

    ##############
    # Draw Network
    ##############

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50,30)
    fig.suptitle(title, fontsize=50) ## change title

    # draw network
    pre_pos_G2 = dict(zip(G2.nodes(), coordinates_G2)) # make a dictionary and assign each node its coordinate point
    pos_G2 = nx.spring_layout(G2, fixed = G2.nodes(), pos=pre_pos_G2) # you have to fix the nodes in place!
    nx.draw_networkx(G2, pos = pos_G2, node_size=node_sizes, arrows=False, with_labels=True, node_color = node_colors, cmap=plt.cm.Blues, edge_color='black', width=1.0/10, style='solid', font_size=8)

    # add xlabel, remove ylabel, set x-margin, set y-margin, set x-ticks
    plt.xlabel("years", fontsize=50)
    y_label = info_type + " " + deg_type
    plt.ylabel(y_label, fontsize=50)
    axes=plt.gca()
    axes.set_xlim([min(X_G2)-1, max(X_G2)+1])
    axes.set_ylim([min(Y_G2)-1, max(Y_G2)+1])
    plt.savefig(save_dir)

    # end timer
    print("--- %s seconds ---" % (time.time() - start_time))

def bigball_spring_layout(graph_object, start_year, end_year, deg_type, info_type, del_zero_deg_nodes, save_dir):
    
    '''
    USAGE: bigball_spring_layout(D, 1980, 1989, 'in_degree', 'mean', False, 'some_directory/plot_test.png')

    NOTE: graph_object should contain 'year' attribute for each node; If not, simply make one from 'date' attribute
        - If no 'year' attribute, your graph_object can't use this function

    start_year, end_year (Int):
        - Use any subset either from 'years_useable(graph_object)' or 'years_useable_after_del(graph_object)'

    deg_type: (String)
        - 'in_degree'
        - 'out_degree'
        - 'degree'

    info_type: (String)
        - 'mean'
        - 'median'
        - 'total'

    del_zero_deg_nodes: (Boolean)
        - True (delete all the nodes with zero degree, while keeping the original degree information of remaining nodes)
        - False (don't delete all the nodes with zero degree)
    '''

    start_time = time.time() # start timer to approximate how long this function takes

    ###############
    # Make Graph G
    ###############
    G = graph_object.copy()

    if del_zero_deg_nodes:
        solitary = [n for n,d in G.degree_iter() if d==0]
        G.remove_nodes_from(solitary)
    
    nodes_to_delete = []
    for each_node in G.nodes():
        if not (start_year <= G.node[each_node]['year'] <= end_year):
            nodes_to_delete.append(each_node)

    G.remove_nodes_from(nodes_to_delete)

    # Get Year Attribute for G.nodes()
    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    # Get Date Attribute for G.nodes()
    dates = []
    cases_without_dates = []
    for each_node in G.nodes():
        if G.node[each_node]['date'] == '':
            cases_without_dates.append(each_node)
        else:
            dates.append(G.node[each_node]['date'])

    # Get node, year information
    nodes_G = G.nodes() ## list of nodes
    year_nodes_tup = zip(years, nodes_G) ## make list of tuples [(year1, node1), ... , (year_n, node_n)]
    year_nodes_tup_sorted = sorted(year_nodes_tup, key=itemgetter(0)) ## sort the above tuples by year in increasing order

    # Turn above information into ordered dictionary
    year_nodes_dict = OrderedDict() ## get a dictionary of { {year: [all the nodes within that year]} , ... , {year: ...} }
    for each_tuple in year_nodes_tup_sorted:
        if not year_nodes_dict.has_key(each_tuple[0]):
            year_nodes_dict[each_tuple[0]] = []
        year_nodes_dict[each_tuple[0]].append(each_tuple[1])
    
    # Big Ball Layout where nodes represent the unique years
    G2 = G.copy()
    for year, list_of_nodes in year_nodes_dict.iteritems():
        G2.add_node(year,
                    num_of_nodes = len(list_of_nodes)
                    )
        for n1, n2, data in G2.edges(data=True):
            if n1 in list_of_nodes:
                G2.add_edge(year, n2, data)
            elif n2 in list_of_nodes:
                G2.add_edge(n1, year, data)

        G2.remove_nodes_from(list_of_nodes)

    #Get Title for Big Ball Layout
    if del_zero_deg_nodes:
        title = str(min(years)) + '-' + str(max(years)) + ' SCOTUS Network with ' + str(G2.number_of_nodes()) + ' Years After Deleting Zero-Degree Nodes in the Entire Network ' + '(colored nodes by ' + info_type + ' ' + deg_type + ')'
    else:
        title = str(min(years)) + '-' + str(max(years)) + ' SCOTUS Network with ' + str(G2.number_of_nodes()) + ' Years ' + '(colored nodes by ' + info_type + ' ' + deg_type + ')'

    # Get node_sizes for drawing the newtork later, which is based on the number of nodes/cases in a year
    node_sizes = []
    for each_node in G2.nodes():
        some_node_size = (G2.node[each_node]['num_of_nodes'])*5 # multiply by 5 for visualization purposes of node sizes
        node_sizes.append(some_node_size)
    
    # Get node, in/out-degree information
    if deg_type == 'in_degree':
        deg_dict = graph_object.in_degree() ## dict of key(node): value(in-degree) in original graph object
    if deg_type == 'out_degree':
        deg_dict = graph_object.out_degree() ## dict of key(node): value(out-degree) in original graph object
    if deg_type == 'degree':
        deg_dict = graph_object.degree() ## dict of key(node): value(degree) in original graph object
    deg_list = [deg_dict[n] for n in nodes_G] ## list of nodes' respective in/out/total-degrees in original graph object
    year_deg_tup = zip(years, deg_list) ## make list of tuples [(year1, in/out/total-deg1) , ... , (year_n, in/out/total-deg_n)] (original graph object)
    year_deg_tup_sorted = sorted(year_deg_tup, key=itemgetter(0)) ## sort the above tuples by year in increasing order (original graph object)

    # Turn above information into ordered dictionary
    year_deg_dict = OrderedDict() ## get a dictionary of { {year: [all the in/out/total_degrees within that year]} , ... , {year: ...} }
    for each_tuple in year_deg_tup_sorted:
        if not year_deg_dict.has_key(each_tuple[0]):
            year_deg_dict[each_tuple[0]] = []
        year_deg_dict[each_tuple[0]].append(each_tuple[1])

    if info_type == 'mean':
        # Get node colors for drawing the network later, which is based on the mean in/out/total-degree of that year
        node_colors = [] ## get the respective mean in/out/total-degree for each year
        for each_year in G2.nodes():
            degs = year_deg_dict[each_year]
            degs_mean = sum(degs)/len(degs)
            node_colors.append(degs_mean)

    if info_type == 'median':
        # Get node colors for drawing the network later, which is based on the median in/out/total-degree of that year
        node_colors = [] ## get the respective mean in/out/total-degree for each year
        for each_year in G2.nodes():
            degs = year_deg_dict[each_year]
            degs_median = np.median(np.array(degs))
            node_colors.append(degs_median)

    if info_type == 'total':
        # Get node colors for drawing the network later, which is based on the total in/out/total-degree of that year
        node_colors = [] ## get the respective mean in/out/total-degree for each year
        for each_year in G2.nodes():
            degs = year_deg_dict[each_year]
            degs_total = sum(degs)
            node_colors.append(degs_total)

    ##############
    # Draw Network
    ##############

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50,30)
    fig.suptitle(title, fontsize=50) ## change title

    # draw network
    pos_G2 = nx.spring_layout(G2, k=3/math.sqrt(len(G2)))
    nx.draw(G2, pos = pos_G2, node_size=node_sizes, arrows=False, with_labels=True, node_color = node_colors, cmap=plt.cm.Blues, edge_color='black', width=1.0/10, style='solid', font_size=8)

    # save plot
    plt.savefig(save_dir)

    # end timer
    print("--- %s seconds ---" % (time.time() - start_time))





def get_nodes_given_year(graph_object, year):
    G = graph_object.copy()
    nodes_to_delete = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] != year:
            nodes_to_delete.append(each_node)

    G.remove_nodes_from(nodes_to_delete)

    return G.nodes()

def get_indegs_given_year(graph_object, year):
    G = graph_object.copy()
    nodes_to_delete = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] != year:
            nodes_to_delete.append(each_node)
    G.remove_nodes_from(nodes_to_delete)

    nodes_in_year = G.nodes()
    in_degrees_all = graph_object.in_degree() ## dict of key(node): value(in-degree) ; keep original in_degree information
    in_degrees_in_year = [in_degrees_all[n] for n in nodes_in_year] ## list of nodes's respective in-degrees in a year

    return in_degrees_in_year

def get_outdegs_given_year(graph_object, year):
    G = graph_object.copy()
    nodes_to_delete = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] != year:
            nodes_to_delete.append(each_node)
    G.remove_nodes_from(nodes_to_delete)

    nodes_in_year = G.nodes()
    out_degrees_all = graph_object.out_degree() ## dict of key(node): value(out-degree) ; keep original out_degree information
    out_degrees_in_year = [out_degrees_all[n] for n in nodes_in_year] ## list of nodes's respective out-degrees in a year

    return out_degrees_in_year

def get_degs_given_year(graph_object, year):
    G = graph_object.copy()
    nodes_to_delete = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] != year:
            nodes_to_delete.append(each_node)
    G.remove_nodes_from(nodes_to_delete)

    nodes_in_year = G.nodes()
    degrees_all = graph_object.degree() ## dict of key(node): value(degree) ; keep original degree information
    degrees_in_year = [degrees_all[n] for n in nodes_in_year] ## list of nodes's respective degrees in a year

    return degrees_in_year

def get_case_metadata(graph_object, case_number):
    '''
    given the CL id, prints out the meta data i.e. the case_name, date, etc.
    '''
    # Note: case_number = node_number (type = int)

    #print graph_object.node[case_number]
    return graph_object.node[case_number]

def open_case_webpage(court_name, case_number):
    '''
    open url from CL website
    '''
    # Note: case_number is int; so convert to string
    #       court_name should be string (court_name = jurisdiction i.e. 'scotus') ; refers to directory file

    proj_cwd = os.path.dirname(os.getcwd())
    data_dir = os.path.join(proj_cwd, 'data')
    juris_dir = os.path.join(data_dir, court_name)
    clusters_dir = os.path.join(juris_dir, 'clusters')
    file_dir = os.path.join(clusters_dir, str(case_number) + r'.json')
    with open(file_dir) as json_file:
        js = json.load(json_file)
    unicode_absolute_url = js['absolute_url'] # "/opinion/1722/shady-grove-orthopedic-associates-p-a-v-allstate-ins-co/"
    string_absolute_url = unicode_absolute_url.encode('utf8')
    case_webpage = "https://www.courtlistener.com" + string_absolute_url
    #return case_webpage
    print 'Opening courtlistener webpage for case ' , case_number , ': ' , case_webpage
    webbrowser.open(case_webpage)