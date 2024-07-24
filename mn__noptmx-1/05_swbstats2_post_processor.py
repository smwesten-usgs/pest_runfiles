#!/usr/bin/env python

'''
May 13, 2024
Script to take swbstats2 output and condense and create a pest-compatible
observation file.

For use on the denali computer system
--> Paths are for denali
Requires access to MN_observed_values_ALL.csv (actual observations) file
for complete names

# M. Nielsen

Edited for MN SWB project, using AET, net infiltraiton, direct runoff and total 
streamflow observations.

'''

# Setup:
import pandas as pd
import os

# Just for testing:

print ('Converting zonal stats to observations')

# ----------------------------------------------------------------
# baseflow/net_infiltration and runoff observations
# ----------------------------------------------------------------
# Read in the zonal stats files from swbstats2:
# ANNUAL and SEASONAL data are in the same files
aet_file = 'zonal_stats__actual_et.csv'
bf_file = 'zonal_stats__net_infiltration.csv'
ro_file = 'zonal_stats__runoff.csv'
ro_file2 = 'zonal_stats__rejected_net_infiltration.csv'
observation_basin_info_file = 'mn__observation_basins_list_with_index.csv'
good_observations = pd.read_csv('mn__observed_values_ALL.csv')

def make_obsnames(obs_df, obstype):  #obstype = prefix for obsname
    
    # Get observation watershed info:
    obstmp = pd.read_csv(observation_basin_info_file)
    obsinfo = obstmp[['BASIN_INDX','site_no']].sort_values(by='BASIN_INDX')

    df1 = pd.merge(obs_df, obsinfo, how='left', left_on='zone_id', right_on='BASIN_INDX')
    df1['year'] = df1['start_date'].str[:4]
    df1['month'] = df1['start_date'].str.split('-').str[1]
    df1['zone_id'] = df1['zone_id'].astype(str)
    df1['site_no'] = df1['site_no'].astype(str)
    # Set up station numbers correctly:
    df1['Station'] = '0' + df1['site_no'].astype(str)
    # This messes up the station numbers for the MN DNR gages, so fix:
    fixes = ['0H10067001','0H11015001','0H12047001','0H16023001','0H17063001','0H18066001',
    '0H18075003','0H21021001','0H38025003','0H39016001']
    df1.loc[(df1['Station'].isin(fixes)),'Station'] = df1['Station'].str[2:]

    
    df1['start_mon'] = df1['start_date'].str[5:7]
    
    # Calculate time delta for the obs:
    df1['start_date']= pd.to_datetime(df1['start_date']) 
    df1['end_date']= pd.to_datetime(df1['end_date']) 

    df1['TimeDelta'] = df1['end_date'] - df1['start_date'] + pd.to_timedelta(1, unit="D")
    df1['days'] = df1['TimeDelta'].astype(str).str.split(' ').str[0].astype(int)  #Have season-type and year-type lengths
    df1['date'] = df1['start_date'].astype(str)

    
    df1['ObsName'] = 'xxxxx'  # Initialize.
    
    # use .loc
    df1.loc[df1.days > 100, 'ObsName'] = obstype + df1['zone_id'] + "_" + df1['Station'] + "_" + df1['year'] #changed
    # ----------------------------------------------
    # days < 100 are seasonal observations:
    # replace month with season:
    seas = ['ann','spr','sum','fall','wint']
    monlist = ['01','03','06','09','12']
    seas_dict = dict(zip(monlist, seas))
    df1['seas'] = df1['month'].map(seas_dict)

    # Replace year with year+1 for winter obs:
    df1.loc[df1.seas == 'wint', 'year'] = (df1['start_date'].dt.year + 1).astype(str)  # if winter, set year to the following year

    df1.loc[df1.days < 100, 'ObsName'] = obstype + df1['zone_id'] + "_" + df1['Station'] + "_" + df1['seas'] + '-' + df1['year']
    # ------------------------------------------

    df2 = df1[['ObsName','start_date','end_date','zone_id','mean_swb','days']].copy()

    return df2


# Read ANNUAL zone stats files:
# ------------------------------------------
tmpdat_aet = pd.read_csv(aet_file)
simdata_aet = tmpdat_aet.loc[tmpdat_aet.count_swb != 0][['start_date','end_date','zone_id','mean_swb']].copy()
simdata_aet.sort_values(by=['zone_id','start_date'], inplace=True)

tmpdat_bf = pd.read_csv(bf_file)
simdata_bf = tmpdat_bf.loc[tmpdat_bf.count_swb != 0][['start_date','end_date','zone_id','mean_swb']].copy()
simdata_bf.sort_values(by=['zone_id','start_date'], inplace=True)

# RUNOFF is two components added together:
# runoff
tmpdat_ro = pd.read_csv(ro_file)
simdata_ro = tmpdat_ro.loc[tmpdat_ro.count_swb != 0][['start_date','end_date','zone_id','mean_swb']].copy()
simdata_ro.sort_values(by=['zone_id','start_date'], inplace=True)
# rejected net infiltration
tmpdat_rni = pd.read_csv(ro_file2)
simdata_rni = tmpdat_rni.loc[tmpdat_rni.count_swb != 0][['start_date','end_date','zone_id','mean_swb']].copy()
simdata_rni.sort_values(by=['zone_id','start_date'], inplace=True)


# Call function to return prettied-up observations:
dat_aet = make_obsnames(simdata_aet, 'aet_')
dat_bf = make_obsnames(simdata_bf, 'bf_')
dat_ro = make_obsnames(simdata_ro, 'ro_')
dat_rni = make_obsnames(simdata_rni, 'rni_')

#print(dat_aet.head())

# Join the runoff and rejected net infiltration and add together:
dat_ro['ID'] = dat_ro['ObsName'].str[3:]
dat_rni['ID'] = dat_rni['ObsName'].str[4:]
dat_ro.set_index('ID', inplace=True)
dat_rni.set_index('ID', inplace=True)
dat_ro_all = pd.merge(dat_ro, dat_rni, left_on='ID', right_on='ID', how='left')
dat_ro_all = dat_ro_all[~dat_ro_all.index.duplicated(keep='first')]
dat_ro_all['ro_tot'] = dat_ro_all['mean_swb_x'] + dat_ro_all['mean_swb_y']
dat_ro_all['mean_swb'] = dat_ro_all['ro_tot']
#print(dat_ro.tail())

# Clean up for merging with the bf:
dat_ro_all = dat_ro_all.reset_index()
dat_ro_all.rename(columns={'ObsName_x':'ObsName',
                          'start_date_x':'start_date',
                          'end_date_x':'end_date',
                          'zone_id_x':'zone_id',
                          'days_x':'days'}, inplace=True)

dat_ro_all = dat_ro_all[['ObsName','start_date','end_date', 'zone_id','mean_swb','days']]
#print(dat_ro_all.tail())

# # Join the total runoff and net infiltration to get "TOTAL" flow analogue
dat_ro_all['ID'] = dat_ro_all['ObsName'].str[3:]
dat_bf['ID'] = dat_bf['ObsName'].str[3:]
dat_ro_all.set_index('ID', inplace=True)
dat_bf.set_index('ID', inplace=True)

dat_totsw = pd.merge(dat_ro_all, dat_bf, left_on='ID', right_on='ID', how='left')
dat_totsw = dat_totsw[~dat_totsw.index.duplicated(keep='first')]
dat_totsw['totsw'] = dat_totsw['mean_swb_x'] + dat_totsw['mean_swb_y']
dat_totsw['mean_swb'] = dat_totsw['totsw']

# Add proper prefix to obsname:
dat_totsw['ObsName'] = 'totsw_' + dat_totsw.index
#print(dat_totsw.tail())

# Clean up for merging with the other obs:
dat_totsw = dat_totsw.reset_index()
dat_totsw.rename(columns={'start_date_x':'start_date',
                          'end_date_x':'end_date',
                          'zone_id_x':'zone_id',
                          'days_x':'days'}, inplace=True)

dat_totsw = dat_totsw[['ObsName','start_date','end_date', 'zone_id','mean_swb','days']]
#print(dat_totsw.tail())
##print(dat_aet.head())


##############################################################
# WEED OUT VAULES WE DIDN"T KEEP
##########################################################
'''Many of the SW values were not deemed "GOOD", and the final set of observations
we want to use is in the file "MN__ALL_SW_OBS_TABLE_final.csv"  This part of the script
deletes SWB output that isn't compatible with the "GOOD" observations.'''

goodobs_short = good_observations[['PEST_name','Obs_Zone']]

dat_bf2 = pd.merge(dat_bf, goodobs_short, how='inner', left_on='ObsName', right_on='PEST_name')
dat_ro2 = pd.merge(dat_ro, goodobs_short, how='inner', left_on='ObsName', right_on='PEST_name')
dat_totsw2 = pd.merge(dat_totsw, goodobs_short, how='inner', left_on='ObsName', right_on='PEST_name')
# AET observed values only go through 2017...
dat_aet2 = pd.merge(dat_aet, goodobs_short, how='inner', left_on='ObsName', right_on='PEST_name')

##########################################################
# # Join ALL aet, ni, ro, totsw  into one file
obsdfs = [dat_aet2,dat_bf2,dat_ro2,dat_totsw2]
obsdat_all = pd.concat(obsdfs)

# clean up
obsdat_all['Value'] = obsdat_all['mean_swb'].round(6)
#del obsdat_all['PEST_name']
#del obsdat_all['Obs_Zone']
#del obsdat_all['mean_swb']

# Sort:
obsdat_all.sort_values(by='ObsName', inplace=True)
print(len(obsdat_all))
print(obsdat_all.info())

# # Save to obs files:
outdat = obsdat_all[['ObsName','Value']].copy()

#outfile1 = 'simulated_values__ALLTIME.obs'
outfile1 = 'simulated_values__ALLDATES_2000to2022.obs'
outdat.to_csv(outfile1, sep=' ', index=False)


print ('Saved obs file: ' + outfile1 )

