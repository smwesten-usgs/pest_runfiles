ptf ~
# OK, the concept here is that we use pest++ to estimate metaparameters (intermediate parameters?), 
# which then get processed by a little Python script to produce the numerical values that SWB2
# actually sees and processes. The idea is that this Python script would allow for some degree
# of structure to be imposed on the resulting SWB2 parameter values. For example, the 
# curve number aligner would be used to take the pest++ generated curve numbers for the 
# appropriate 'a' soils and produce the values needed for 'b', 'c', and 'd' soils, as well as the 
# mixed soil classes. Recall that our current thinking is that if the landuse is agricultural in nature,
# it is highly likely that the soils are in the 'drained' condition; conversely, if the landuse is 
# 'natural' it is likely 'undrained' (a 'D' soil).)

[curve_numbers]
corn = ~corn_base-cn~
soybn = ~soybn_base-cn~
alfalf = ~alfalf_base-cn~
smgrn = ~smgrn_base-cn~
decfrst = ~decfrst_base-cn~
evfrst = ~evfrst_base-cn~
mixfrst = ~mixfrst_base-cn~
pasture = ~pasture_base-cn~
wdwetl = ~wdwetl_base-cn~
hbwetl = ~hbwetl_base-cn~

[rooting_depths]
corn = ~corn_base-rz~
soybn = ~soybn_base-rz~
alfalf = ~alfalf_base-rz~
smgrn = ~smgrn_base-rz~
decfrst = ~decfrst_base-rz~
evfrst = ~evfrst_base-rz~
mixfrst = ~mixfrst_base-rz~
pasture = ~pasture_base-rz~
wdwetl = ~wdwetl_base-rz~
hbwetl = ~hbwetl_base-rz~

[max_net_infiltration]
corn = ~corn_base-max-ni~
soybn = ~soybn_base-max-ni~
alfalf = ~alfalf_base-max-ni~
smgrn = ~smgrn_base-max-ni~
decfrst = ~decfrst_base-max-ni~
evfrst = ~evfrst_base-max-ni~
mixfrst = ~mixfrst_base-max-ni~
pasture = ~pasture_base-max-ni~
wdwetl = ~wdwetl_base-max-ni~
hbwetl = ~hbwetl_base-max-ni~

[max_net_infiltration_multipliers]
max_net_infil_mult_ab = ~max_net_infil_mult_ab~
max_net_infil_mult_ac = ~max_net_infil_mult_ac~
max_net_infil_mult_ad = ~max_net_infil_mult_ad~

[rooting_depth_multipliers]
rooting_depth_mult_ab = ~rooting_depth_mult_ab~
rooting_depth_mult_ac = ~rooting_depth_mult_ac~
rooting_depth_mult_ad = ~rooting_depth_mult_ad~