'''Parameter processor for curve numbers, max net infiltration, and rooting depths.
begins with PEST-established values for "A" soils and broadcasts out to "B", "C", and "C" 
soils.

Files needed:
'pest_intermediate_parameters.toml'  - parameter upgrades from PEST for "A" soils
'MN__LU_lookup_table_with_PARS__SMW.txt.tpl'  - lookup table from PEST that has variables
     for this script in ${}$ format.  (File has PEST upgrade values for ~ {} ~ PEST parameters)

'''
import tomli
import numpy as np
import argparse

input_parameter_filename = 'pest_intermediate_parameters.toml'
input_template_filename = 'mn__lu_lookup_table.txt.template'
output_swb_lookup_table_filename = 'mn__lu_lookup_table.txt'

def net_infiltration_aligner(max_net_infil_a, 
                             dict_prefix = 'max_net_infil_',
                             net_infil_factors=[0.5, 0.3, 0.15],
                             condition='drained',
                             num_digits=3):
    """
    Implementation of a method for enforcing stucture on net_infiltration. The 
    ratios applied between the soil groups is user-defined.

    Args:
        net_infil_a (str): _description_
        dict_prefix (str, optional): _description_. Defaults to 'net_infil_'.
        net_infil_factors (list, optional): _description_. Defaults to [0.5, 0.3, 0.15].
        condition (str, optional): _description_. Defaults to 'drained'.

    Returns:
        dict: dictionary containing maximum net infiltration rates for b-d and dual-classification soil groups
    """

    ni_a = np.round(max_net_infil_a, decimals=num_digits)
    ni_b = np.round(max_net_infil_a * net_infil_factors[0], decimals=num_digits)
    ni_c = np.round(max_net_infil_a * net_infil_factors[1], decimals=num_digits)
    ni_d = np.round(max_net_infil_a * net_infil_factors[2], decimals=num_digits)

    if condition == 'drained':
        ni_ad = ni_a
        ni_bd = ni_b
        ni_cd = ni_c
    else:
        ni_ad = ni_d
        ni_bd = ni_d
        ni_cd = ni_d

    result_dict= {f"{dict_prefix}a": ni_a,
                  f"{dict_prefix}b": ni_b,
                  f"{dict_prefix}c": ni_c,
                  f"{dict_prefix}d": ni_d,
                  f"{dict_prefix}ad": ni_ad,
                  f"{dict_prefix}bd": ni_bd,
                  f"{dict_prefix}cd": ni_cd}

    return result_dict

def curve_number_aligner(curve_number_a, 
                         dict_prefix = 'cn_',
                         condition='drained',
                         num_digits=3):
    """
    Implementation of the 'curve number aligner'. 
    see page 13 of Hawkins, R.H., Ward, T.J., Woodward, D.E., and Van Mullem, J.A., 2009, 
    Curve number hydrology: American Society of Civil Engineers, 106 p.

    Maximum theoretical value for an 'A' soil is 77. This is not enforced in the curve number aligner.
    """

    curve_number_b = np.round(min([37.8 + 0.622 * curve_number_a, 100.]), decimals=num_digits)
    curve_number_c = np.round(min([58.9 + 0.411 * curve_number_a, 100.]), decimals=num_digits)
    curve_number_d = np.round(min([67.2 + 0.328 * curve_number_a, 100.]), decimals=num_digits)

    if condition == 'drained':
        curve_number_ad = np.round(curve_number_a, decimals=num_digits)
        curve_number_bd = curve_number_b
        curve_number_cd = curve_number_c
    else:
        curve_number_ad = curve_number_d
        curve_number_bd = curve_number_d
        curve_number_cd = curve_number_d

    result_dict= {f"{dict_prefix}a": np.round(curve_number_a, decimals=num_digits),
                  f"{dict_prefix}b": curve_number_b,
                  f"{dict_prefix}c": curve_number_c,
                  f"{dict_prefix}d": curve_number_d,
                  f"{dict_prefix}ad": curve_number_ad,
                  f"{dict_prefix}bd": curve_number_bd,
                  f"{dict_prefix}cd": curve_number_cd}

    return result_dict


def root_zone_aligner(root_zone_depth_a, 
                      dict_prefix = 'rz_',
                      root_zone_factors=[1.25, 1.0, 0.666],
                      condition='drained',
                      num_digits=3):
    """
    Implementation of a method for enforcing stucture on root zone depths. The 
    ratios applied between the soil groups roughly follows the relations given in 
    table 10 of Thornthwaite and Mather (1957). In that publication, there is a
    suggestion that the maximum rooting depth is associated with the 'B' soil group,
    with the rooting depth for 'C' and 'D' soils significantly smaller than those
    for the 'B' soil group.

    Args:
        root_zone_depth_a (_type_): _description_
        dict_prefix (str, optional): _description_. Defaults to 'rz_'.
        root_zone_factors (list, optional): _description_. Defaults to [1.25, 1.0, 0.666].
        condition (str, optional): _description_. Defaults to 'drained'.

    Returns:
        dict: dictionary containing rooting depths for b-d and dual-classification soil groups
    """

    rz_a = np.round(root_zone_depth_a, decimals=num_digits)
    rz_b = np.round(root_zone_depth_a * 1.25, decimals=num_digits)
    rz_c = np.round(root_zone_depth_a, decimals=num_digits)
    rz_d = np.round(root_zone_depth_a * 0.666, decimals=num_digits)

    if condition == 'drained':
        rz_ad = rz_a
        rz_bd = rz_b
        rz_cd = rz_c
    else:
        rz_ad = rz_d
        rz_bd = rz_d
        rz_cd = rz_d

    result_dict= {f"{dict_prefix}a": rz_a,
                  f"{dict_prefix}b": rz_b,
                  f"{dict_prefix}c": rz_c,
                  f"{dict_prefix}d": rz_d,
                  f"{dict_prefix}ad": rz_ad,
                  f"{dict_prefix}bd": rz_bd,
                  f"{dict_prefix}cd": rz_cd}

    return result_dict


# read in the file of parameters estimated by pest++
with open(input_parameter_filename, "rb") as f:
    param_dict = tomli.load(f)

replacements = dict()

# read in the max net infiltration multipliers from the TOML file
max_net_infil_mult_ab = param_dict['max_net_infiltration_multipliers']['max_net_infil_mult_ab']
max_net_infil_mult_ac = param_dict['max_net_infiltration_multipliers']['max_net_infil_mult_ac']
max_net_infil_mult_ad = param_dict['max_net_infiltration_multipliers']['max_net_infil_mult_ad']

# read in the rooting depth multipliers from the TOML file
rooting_depth_mult_ab = param_dict['rooting_depth_multipliers']['rooting_depth_mult_ab']
rooting_depth_mult_ac = param_dict['rooting_depth_multipliers']['rooting_depth_mult_ac']
rooting_depth_mult_ad = param_dict['rooting_depth_multipliers']['rooting_depth_mult_ad']

param_groups = ['corn','soybn','alfalf','smgrn','decfrst','mixfrst','evfrst',
                'pasture','wdwetl','hbwetl']

drained_condition = {'corn': 'drained',
                     'soybn': 'drained',
                     'alfalf': 'drained',
                     'smgrn': 'drained',
                     'decfrst': 'undrained',
                     'mixfrst': 'undrained',
                     'evfrst': 'undrained',
                     'pasture': 'undrained',
                     'wdwetl': 'undrained',
                     'hbwetl': 'undrained'}

for group in param_groups:
    cn = param_dict['curve_numbers'][group]
    cn_dict = curve_number_aligner(curve_number_a=cn,
                                    dict_prefix=f"{group}_cn_",
                                    condition=drained_condition[group])
    replacements.update(cn_dict)

    rz = param_dict['rooting_depths'][group]
    rz_dict = root_zone_aligner(root_zone_depth_a=rz,
                                    dict_prefix=f"{group}_rz_",
                                    root_zone_factors=[rooting_depth_mult_ab,
                                                       rooting_depth_mult_ac,
                                                       rooting_depth_mult_ad],
                                    condition=drained_condition[group])
    replacements.update(rz_dict)

    ni = param_dict['max_net_infiltration'][group]
    ni_dict = net_infiltration_aligner(max_net_infil_a=ni,
                                        dict_prefix=f"{group}_max_net_infil_",
                                        net_infil_factors=[max_net_infil_mult_ab,
                                                           max_net_infil_mult_ac,
                                                           max_net_infil_mult_ad],
                                        condition=drained_condition[group])
    replacements.update(ni_dict)

    # # add the multipliers to the replacements dictionary to ensure they are
    # # written to the 'parameter-processor-derived-par-vals
    # multipliers_dict = {'max_net_infil_ab': max_net_infil_ab,
    #                     'max_net_infil_ac': max_net_infil_ac,
    #                     'max_net_infil_ad': max_net_infil_ad,
    #                     'rooting_depth_ab': rooting_depth_ab,
    #                     'rooting_depth_ac': rooting_depth_ac,
    #                     'rooting_depth_ad': rooting_depth_ad}
    
    # replacements.update(multipliers_dict)

# substitute in the replacement values, using the *.tpl file as the basis for the resulting
# file structure and content
with (open(input_template_filename, ) as infile, 
        open(output_swb_lookup_table_filename , 'w') as outfile):
    for line in infile:
        if 'ptf' in line:
            continue
        for src, target in replacements.items():
            line = line.replace(f"${src}$", str(target))
        outfile.write(line)

with (open('parameter-processor-derived-par-vals.obs', 'w')) as obsfile:
    obsfile.write(f"obsnme obsval\n") 
    for src, target in replacements.items():
        obsfile.write(f"{src} {target}\n")

with(open('parameter-processor-derived-par-vals.ins', 'w')) as insfile:
    insfile.write(f"pif ~\n")
    insfile.write(f"l1\n")
    for src, target in replacements.items():
        insfile.write(f"~{src}~ !{src}!\n")
