##This code is for finding the percentage of the nodes accessible from 
## the LTS = 1 paths in Dorval and Point-Clair area. 
## (Winter and Summer Paths are seperated.)

### accessibility
import networkx as nx
import pdb, os
import pandas as pd
from progressbar import progressbar
#import multiprocessing
#multiprocessing.cpu_count()

### change the directory
os.chdir(r'F:\bike.proj\nov13')
print("Current Working Directory " , os.getcwd())

#Loading the shape files. 
all_ways = nx.read_shp('dorval_all3.shp')
tw0_ways = nx.read_shp('dorval_sens0_5.shp')

summer_lts1 = nx.read_shp('summer_8.shp')
summer_twoW = nx.read_shp('summer_sens0_8.shp')

winter_lts1 = nx.read_shp('dorval_winter3.shp')
winter_twoW = nx.read_shp('dorva_sens0_winter3.shp')

# Completeing the network by adding the reverse part of two-way streets.
all_network = nx.compose(all_ways,tw0_ways.reverse(copy=False))
summer_network = nx.compose(summer_lts1,summer_twoW.reverse(copy=False))
winter_network = nx.compose(winter_lts1,winter_twoW.reverse(copy=False))

summer_network.number_of_edges() #For checking
summer_network.number_of_nodes() #For checking

aaa = nx.shortest_path(all_network)
e = aaa.keys() 
# Getting all the nodes
def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)
          
    return list

ee = getList(aaa)
a = sorted(ee)
atod = pd.DataFrame()
atod_all = pd.DataFrame()
# Getting nodes' Latitude & Longitude
for i in progressbar(range(len(a))):
    atod = pd.DataFrame({'x':[float(a[i][0])], 'y':[float(a[i][1])] })
    atod_all = atod_all.append(atod, ignore_index = True).drop_duplicates()

one_node = pd.DataFrame()
all_nodes = pd.DataFrame()

## Finding out how many nodes each node is connected with.
def path(i, j):
    #path_r = list()
    #try:
    #    path_r = nx.shortest_path(all_network, source= i ,target= j, weight='length')
    #except nx.NetworkXNoPath:
    #    path_r = -99
    ##All nodes network
    try:
        path_d = nx.bellman_ford_path_length(all_network, source= i,  target= j, weight='length')
    except nx.NetworkXNoPath:
        path_d = -99
    ##Summer network
    try:
        path_d_summer = nx.bellman_ford_path_length(summer_network, source= i,  target= j, weight='length')
    except (nx.NetworkXNoPath, nx.NodeNotFound) :
        path_d_summer = -99
    ##Winter network
    try:
        path_d_winter = nx.bellman_ford_path_length(winter_network, source= i,  target= j, weight='length')
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        path_d_winter = -99
          
    return   path_d_summer, path_d_winter,path_d

## Calculating the percentage of accessible nodes.
measure_all_nodes = pd.DataFrame()
for h in progressbar(range(len(a))):
    all_one_node = pd.DataFrame()
    i = a[h]
    for j in a:
        [path_d_summer, path_d_winter,path_d] = path(i, j) 
        one_node = [i, j, path_d, path_d_summer, path_d_winter]
        one_node = pd.DataFrame( {'from_x':[i[0]], 'from_y':[i[1]],'to_x':[j[0]], 'to_y':[j[1]], 'summer_d':[path_d_summer]}) #'unrestricted_d':[path_d] , 'winter_d':[path_d_winter]
        all_one_node = all_one_node.append(one_node, ignore_index = True).drop_duplicates()
        
        measure1_summer = len(all_one_node.loc[all_one_node['summer_d'] > 0])/len(all_one_node) *100
        measure1_winter = len(all_one_node.loc[all_one_node['winter_d'] > 0])/len(all_one_node) *100
        
        #haveRout = all_one_node.loc[all_one_node['unrestricted_d'] > 0]
        #measure2_summer = max(measure1_summer, (len(haveRout.loc[haveRout['summer_d'] >= 1.1*haveRout['unrestricted_d']])/len(all_one_node) *100))
        #measure2_winter = max(measure1_winter, (len(haveRout.loc[haveRout['winter_d'] >= 1.1*haveRout['unrestricted_d']])/len(all_one_node) *100))
        
        measure1_diff =  measure1_winter - measure1_summer
        #measure2_diff =  measure2_winter - measure2_summer
        
        measure_one_node = pd.DataFrame({'from_x':[i[0]], 'from_y':[i[1]], 'measure1_summer': measure1_summer}) #, , 'measure1_winter':measure1_winter, 'measure2_summer':measure2_summer,'measure2_winter':measure2_winter,'measure1_diff':measure1_diff,'measure2_diff':measure2_diff
        all_nodes = all_nodes + (one_node,)
    measure_all_nodes =  measure_all_nodes.append(measure_one_node, ignore_index = True).drop_duplicates()


measure_all_nodes.to_csv(r'measures_dec19_adding36_golf.csv', index = False, header=True)
#pdb.set_trace()



