#Link dection between dual carriage-ways for intersections, retrying Nov 3, 2021
import pdb, os
import pandas as pd
from colorama import init
init()
from progressbar import progressbar
pdb.set_trace()

os.chdir(r'F:\bike.proj\Link_detection')
print("Current Working Directory " , os.getcwd())

###Intersection joined buffers###
file = os.path.join (os.getcwd(),'inter_joined3nov_2.csv')
data1=pd.read_csv(file,  sep=',', encoding='latin-1')
data1 = data1.loc[data1['SENS_CIR'] != 0].reset_index().drop(columns=['index'])
data1 = data1.loc[data1['SENS_CIR_3'] != 0].reset_index().drop(columns=['index'])
data1 = data1.loc[data1['ID_TRC'] != data1['ID_TRC_3']].reset_index().drop(columns=['index'])
data1=data1[['ID_TRC', 'NOM_VOIE','SENS_CIR', 'ID_TRC_3','NOM_VOIE_3','SENS_CIR_3']]


i_d = pd.read_csv(file,  sep=',', encoding='latin-1')
intersect_pair=  i_d[['ID_TRC', 'ID_TRC_2']].drop_duplicates()

###Midpoint joined buffers###
file2 = os.path.join (os.getcwd(),'midpoint_30m_joined3nov.csv')
data2=pd.read_csv(file2,  sep=',', encoding='latin-1')
data2 = data2.loc[data2['SENS_CIR'] != 0].reset_index().drop(columns=['index'])
data2 = data2.loc[data2['SENS_CIR_2'] != 0].reset_index().drop(columns=['index'])
data2 = data2.loc[data2['ID_TRC'] != data2['ID_TRC_2']].reset_index().drop(columns=['index'])
data2=data2[['ID_TRC', 'NOM_VOIE','SENS_CIR', 'ID_TRC_2','NOM_VOIE_2','SENS_CIR_2']]

a = sorted(list(set(data1['ID_TRC'].unique())))
match = pd.DataFrame()
all_id = pd.DataFrame()


for h in progressbar(range(len(a))):
		match = pd.DataFrame()
		i = a[h]
		inters_data = data1.loc[data1['ID_TRC'] == i].reset_index().drop(columns=['index'])
		mid_data = data2.loc[data2['ID_TRC'] == i].reset_index()
		for t in range(len(inters_data)):
			for j in range( len(mid_data)):
				if (inters_data['ID_TRC_3'][t] == mid_data['ID_TRC_2'][j] and inters_data['NOM_VOIE'][t] == inters_data['NOM_VOIE_3'][t] and inters_data['SENS_CIR'][t] != inters_data['SENS_CIR_3'][t]):
				 match = inters_data.loc[[t]]
		all_id = pd.concat([all_id, match], ignore_index=True).drop_duplicates()
		all_id = all_id.loc[all_id['NOM_VOIE'] != 'Non-00'].reset_index().drop(columns=['index'])

id_dual= all_id[['ID_TRC']]
id_dual2= all_id[['ID_TRC_3']]
id_dual2.rename(columns={'ID_TRC_3': 'ID_TRC'}, inplace=True)
id_dual = id_dual.append(id_dual2, ignore_index = True).drop_duplicates()
id_dual['Dual'] = 1

id_dual.to_csv(r'dual_carriage_nov4.csv', index = False, header=True)

####Check for intersection###
id_dual= all_id[['ID_TRC']]
id_dual2= all_id[['ID_TRC_3']]
id_dual_pair = pd.concat([id_dual, id_dual2] , axis=1)
intersect_pair
id_dual_pair['intersect?'] = 0

aa = sorted(list(set(id_dual_pair['ID_TRC'].unique())))
int_all = pd.DataFrame()

for h in progressbar(range(len(aa))):
		match = pd.DataFrame()
		i = aa[h]
		int1 = id_dual_pair.loc[id_dual_pair['ID_TRC'] == i].reset_index().drop(columns=['index'])
		int2 = intersect_pair.loc[intersect_pair['ID_TRC'] == i].reset_index()
		for t in range(len(int1)):
			for j in range( len(int2)):
				if (int1['ID_TRC'][t] == int2['ID_TRC'][j] and int1['ID_TRC_3'][t] == int2['ID_TRC_2'][j]):
				 int1['intersect?'][t] = 1
		int_all = pd.concat([int_all, int1], ignore_index=True).drop_duplicates()
        
id_dual3= int_all[['ID_TRC', 'intersect?']]
id_dual4= int_all[['ID_TRC_3', 'intersect?']]
id_dual4.rename(columns={'ID_TRC_3': 'ID_TRC'}, inplace=True)
id_dual5 = id_dual3.append(id_dual4, ignore_index = True).drop_duplicates()


id_dual5.to_csv(r'intersecting_links_nov3.csv', index = False, header=True)
