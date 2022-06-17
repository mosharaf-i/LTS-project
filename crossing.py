### Finding LTS at the crossings (different than segment LTS)
import pdb, os
import pandas as pd
from progressbar import progressbar

#Directory
os.chdir(r'F:\bike.proj\crossing')
print("Current Working Directory " , os.getcwd())

#Loading the files
# 1. the crossing data
file1 = os.path.join (os.getcwd(),'cross_dec16.csv')
cross=pd.read_csv(file1,  sep=',', encoding='latin-1')

# 2. The ADT and ID data
file2 = os.path.join (os.getcwd(),'aimsun_idtrc.csv')
trc_aimsun=pd.read_csv(file2,  sep=',', encoding='latin-1')

# 3. Turning volume data (with different IDs)
file3 = os.path.join (os.getcwd(),'turning_volumes.csv')
turn=pd.read_csv(file3,  sep=',', encoding='latin-1')

# 4.LTS data of the segments
file4 = os.path.join (os.getcwd(),'LTS_dec11.csv')
link_lts=pd.read_csv(file4,  sep=',', encoding='latin-1')

##for every junction##
## 1. one movement
# First we need to find out each movement includes which segments and which IDs
a = sorted(list(set(cross['f_ID_TRC'].unique())))

cross['f_ID_TRC_1'] = -99
cross['f_ID_TRC_2'] = -99
cross['t_ID_TRC_1'] = -99
cross['t_ID_TRC_2'] = -99
cross['c_ID_TRC_1'] = -99
cross['c_ID_TRC_2'] = -99

for i in progressbar(range(len(cross))):
    aa = cross['f_ID_TRC'][i].split(',', 1)
    if len(aa) ==1 :
        a1 = float(cross['f_ID_TRC'][i].split('[', 2)[2].split(']', 2)[0])
        a2 = float(-99)
    else:
        a1 = float(cross['f_ID_TRC'][i].split(',', 1)[0].split('[', 3)[2].split(']', 1)[0])
        a2 = float(cross['f_ID_TRC'][i].split(',', 1)[1].split('[', 1)[1].split(']', 2)[0])
    cross['f_ID_TRC_1'][i] = a1
    cross['f_ID_TRC_2'][i] = a2
    bb = cross['t_ID_TRC'][i].split(',', 1)
    if len(bb) ==1 :
        b1 = float(cross['t_ID_TRC'][i].split('[', 2)[2].split(']', 2)[0])
        b2 = float(-99)
    else:
        b1 = float(cross['t_ID_TRC'][i].split(',', 1)[0].split('[', 3)[2].split(']', 1)[0])
        b2 = float(cross['t_ID_TRC'][i].split(',', 1)[1].split('[', 1)[1].split(']', 2)[0])
    cross['t_ID_TRC_1'][i] = b1
    cross['t_ID_TRC_2'][i] = b2
    cc = cross['c_ID_TRC'][i].split(',', 1)
    if len(cc) == 1 :
        c1 = float(cross['c_ID_TRC'][i].split('[', 2)[2].split(']', 2)[0])
        c2 = float(-99)
    else:
        c1 = float(cross['c_ID_TRC'][i].split(',', 1)[0].split('[', 3)[2].split(']', 1)[0])
        c2 = float(cross['c_ID_TRC'][i].split(',', 1)[1].split('[', 1)[1].split(']', 2)[0])
    cross['c_ID_TRC_1'][i] = c1
    cross['c_ID_TRC_2'][i] = c2

#Second, we need to map the IDs between the two ID files, to get the 
# right-turn volumes
move_all = pd.DataFrame()
for j in progressbar(range(len(cross))):
    RT_vol = pd.DataFrame()
    f_cor_aimsun2 = pd.Series()
    c_cor_aimsun2 = pd.Series()
    move_from = cross.loc[[j]]
    from1_id = float(move_from['f_ID_TRC_1'])
    from2_id = float(move_from['f_ID_TRC_2'])
    c1_id = float(move_from['c_ID_TRC_1'])
    c2_id = float(move_from['c_ID_TRC_2'])
    ##from 1
    f_cor_aimsun1 = pd.Series(trc_aimsun.loc[trc_aimsun['c_ID_trc'] == from1_id].reset_index().drop(columns=['index'])['id'])
    try:
        f_cor_aimsun1_1 = float(f_cor_aimsun1[0])
    except KeyError:
        f_cor_aimsun1_1 = -88
        
    if len(f_cor_aimsun1) > 1:
        try:
            f_cor_aimsun1_2 = float(f_cor_aimsun1[1])
        except KeyError:
            f_cor_aimsun1_2 = -88
    else:
        f_cor_aimsun1_2 = float(-99)
    ##cross 1
    c_cor_aimsun1 = pd.Series(trc_aimsun.loc[trc_aimsun['c_ID_trc'] == c1_id].reset_index().drop(columns=['index'])['id'])
    try:
        c_cor_aimsun1_1 = float(c_cor_aimsun1[0])
    except KeyError:
        c_cor_aimsun1_1 = -88
        
    if len(c_cor_aimsun1) > 1:
        try:
            c_cor_aimsun1_2 = float(c_cor_aimsun1[1])
        except KeyError:
            c_cor_aimsun1_2 = -88
    else:
        c_cor_aimsun1_2 = float(-99)
    ##from 2
    if from2_id != -99:
        f_cor_aimsun2 = pd.Series(trc_aimsun.loc[trc_aimsun['c_ID_trc'] == from2_id].reset_index().drop(columns=['index'])['id'])
        try:
            f_cor_aimsun2_1 = float(f_cor_aimsun2[0])
        except KeyError:
            f_cor_aimsun2_1 = -88
    else:
        f_cor_aimsun2_1 = float(-99)
    if len(f_cor_aimsun2) > 1:
        try:
            f_cor_aimsun2_2 = float(f_cor_aimsun2[1])
        except KeyError:
            f_cor_aimsun2_2 = -88
    else:
        f_cor_aimsun2_2 = float(-99)
    ##cross 2
    if c2_id != -99:
        c_cor_aimsun2 = pd.Series(trc_aimsun.loc[trc_aimsun['c_ID_trc'] == c2_id].reset_index().drop(columns=['index'])['id'])
        try:
            c_cor_aimsun2_1 = float(c_cor_aimsun2[0])
        except KeyError:
            c_cor_aimsun2_1 = -88
    else:
        c_cor_aimsun2_1 = float(-99)
        
    if len(c_cor_aimsun2) > 1:
        try:
            c_cor_aimsun2_2 = float(c_cor_aimsun2[1])
        except KeyError:
            c_cor_aimsun2_2 = -88
    else:
        c_cor_aimsun2_2 = float(-99)
    
    t_vol1 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun1_1) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun1_1)].reset_index().drop(columns=['index'])
    t_vol2 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun1_1) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun1_2)].reset_index().drop(columns=['index'])
    t_vol3 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun1_1) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun2_1)].reset_index().drop(columns=['index'])
    t_vol4 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun1_1) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun2_2)].reset_index().drop(columns=['index'])
    
    t_vol5 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun1_2) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun1_1)].reset_index().drop(columns=['index'])
    t_vol6 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun1_2) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun1_2)].reset_index().drop(columns=['index'])
    t_vol7 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun1_2) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun2_1)].reset_index().drop(columns=['index'])
    t_vol8 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun1_2) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun2_2)].reset_index().drop(columns=['index'])
    
    t_vol9 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun2_1) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun1_1)].reset_index().drop(columns=['index'])
    t_vol10 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun2_1) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun1_2)].reset_index().drop(columns=['index'])
    t_vol11 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun2_1) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun2_1)].reset_index().drop(columns=['index'])
    t_vol12 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun2_1) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun2_2)].reset_index().drop(columns=['index'])
    
    t_vol13 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun2_2) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun1_1)].reset_index().drop(columns=['index'])
    t_vol14 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun2_2) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun1_2)].reset_index().drop(columns=['index'])
    t_vol15 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun2_2) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun2_1)].reset_index().drop(columns=['index'])
    t_vol16 = turn.loc[(turn['Export_Turn_section_from_to_fromsection'] == f_cor_aimsun2_2) & (turn['Export_Turn_section_from_to_tosection'] == c_cor_aimsun2_2)].reset_index().drop(columns=['index'])
    
    RT_vol = pd.concat([t_vol1, t_vol2, t_vol3, t_vol4,t_vol5, t_vol6, t_vol7, t_vol8,t_vol9, t_vol10, t_vol11, t_vol12,t_vol13, t_vol14, t_vol15, t_vol16], ignore_index=True)
    vol_max = ((RT_vol[['Vol5h', 'Vol6h', 'Vol7h', 'Vol8h','Vol15h', 'Vol16h', 'Vol17h', 'Vol18h' ]]).max()).max()
    move_from['RT_vol'] = vol_max
    if (f_cor_aimsun1_1 == -88 or f_cor_aimsun1_2 ==-88 or f_cor_aimsun2_1 ==-88 or f_cor_aimsun2_2 ==-88 or c_cor_aimsun1_1 ==-88 or c_cor_aimsun1_2 ==-88 or c_cor_aimsun2_1 ==-88 or c_cor_aimsun2_2 ==-88):
        move_from['not_exist'] = 1
    move_all = move_all.append(move_from, ignore_index = True).drop_duplicates()
    

###LTS inputing: Getting the LTS of the crossing by choosing the LTS of the 
### from-segment.

moveLTS_all = pd.DataFrame()
for j in progressbar(range(len(move_all))):
    move_lts = pd.DataFrame()
    f_lts1 = pd.DataFrame()
    f_lts2 = 0
    c_lts1 = pd.DataFrame()
    c_lts2 = 0
    move_lts = move_all.loc[[j]]
    from1_id = float(move_lts['f_ID_TRC_1'])
    from2_id = float(move_lts['f_ID_TRC_2'])
    c1_id = float(move_lts['c_ID_TRC_1'])
    c2_id = float(move_lts['c_ID_TRC_2'])
    ##from 1
    f_lts1 = link_lts.loc[link_lts['ID_TRC'] == from1_id].reset_index().drop(columns=['index'])

    ##cross 1
    c_lts1 = link_lts.loc[link_lts['ID_TRC'] == c1_id].reset_index().drop(columns=['index'])

    ##from 2
    if from2_id != -99:
        f_lts2 =link_lts.loc[link_lts['ID_TRC'] == from2_id].reset_index().drop(columns=['index'])
    else:
        f_lts2 = -99
        
    ##cross 2
    if c2_id != -99:
        c_lts2 = link_lts.loc[link_lts['ID_TRC'] == c2_id].reset_index().drop(columns=['index'])
    else:
        c_lts2 = -99
        
    #if len(f_lts1)>0:
    #    move_lts['AppLTS_1'] = f_lts1['lts'][0]
    #else:
    #    move_lts['AppLTS_1'] = -99 
        
    if len(c_lts1)>0:
        move_lts['ADT_1'] = c_lts1['ADT'][0]
        move_lts['Q85_1'] = c_lts1['Q85'][0]
        move_lts['NBLane_1'] = c_lts1['NBLane'][0]
        move_lts['SENS_CIR_1'] = c_lts1['SENS_CIR'][0]
    else:
        move_lts['ADT_1'] = -99
        move_lts['Q85_1'] = -99
        move_lts['NBLane_1'] = -99
        move_lts['SENS_CIR_1'] = -99
    
    ###second lts s
    #if isinstance(f_lts2 , pd.DataFrame) and len(f_lts2)>0:
    #    move_lts['AppLTS_2'] = f_lts2['lts'][0]
    #else:
    #    move_lts['AppLTS_2'] = -99
        
    if isinstance(c_lts2 , pd.DataFrame) and len(c_lts2)>0:
        move_lts['ADT_2'] = c_lts2['ADT'][0]
        move_lts['Q85_2'] = c_lts2['Q85'][0]
        move_lts['NBLane_2'] = c_lts2['NBLane'][0]
        move_lts['SENS_CIR_2'] = c_lts2['SENS_CIR'][0]
    else:
        move_lts['ADT_2'] = -99
        move_lts['Q85_2'] = -99
        move_lts['NBLane_2'] = -99
        move_lts['SENS_CIR_2'] = -99
        
    moveLTS_all = moveLTS_all.append(move_lts, ignore_index = True).drop_duplicates()

moveLTS_all.to_csv(r'intersection_input_Dec16.csv', index = False, header=True)
pdb.set_trace()

### ADT fix #####
### Putting ADT for the legs with only one ADT input.
#####################
file1 = os.path.join (os.getcwd(),'intersection_input_Dec16.csv')
cross=pd.read_csv(file1,  sep=',', encoding='latin-1')
cross['ADT_leg'] = 0
for i in progressbar(range(len(cross))):
    if (cross['ADT_2'][i] != -99) or (cross['ADT_2'][i] != -8888) :
        cross['ADT_leg'][i] = cross['ADT_1'][i] + cross['ADT_2'][i]
    else:
        cross['ADT_leg'][i] = cross['ADT_1'][i]
        
        
## Puttin the width of the islands
cross['XileStop'] = float(-99)
for i in progressbar(range(len(cross))):
    if (cross['c_ID_TRC_2'][i] == -99) :
        cross['XileStop'][i] = -99
    else:
        cross['XileStop'][i] = 1.7

cross.to_csv(r'intersection_input_Dec16_2.csv', index = False, header=True)
