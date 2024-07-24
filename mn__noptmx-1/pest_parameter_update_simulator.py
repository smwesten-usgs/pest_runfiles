import numpy as np

param_groups = ['corn_base','soybn_base', 'alfalf_base', 'smgrn_base', 'decfrst_base',
                'mixfrst_base','evfrst_base', 'pasture_base','wdwetl_base','hbwetl_base']

replacements = dict()

# pretend values for CURVE NUMBERs
for param_group in param_groups:
    key = f"~{param_group}-cn~"
    value = np.random.uniform(low=30., high=77.)
    replacements[key] = value

# pretend values for ROOTING_DEPTHS
for param_group in param_groups:
    key = f"~{param_group}-rz~"
    value = np.random.uniform(low=1., high=4.)
    replacements[key] = value

# pretend values for MAX_NET_INFILTRATION
for param_group in param_groups:
    key = f"~{param_group}-max-ni~"
    value = np.random.uniform(low=2., high=5.)
    replacements[key] = value

# pretend values for the max_net_multipliers
replacements['~max_net_infil_ab~'] = np.random.uniform(low=0.25, high=0.5)
replacements['~max_net_infil_ac~'] = np.random.uniform(low=0.1, high=0.25)
replacements['~max_net_infil_ad~'] = np.random.uniform(low=0.01, high=0.1)

# pretend values for the rooting_zone multipliers
replacements['~rooting_depth_ab~'] = np.random.uniform(low=0.8, high=1.2)
replacements['~rooting_depth_ac~'] = np.random.uniform(low=0.75, high=1.05)
replacements['~rooting_depth_ad~'] = np.random.uniform(low=0.7, high=0.95)

with open('pest_intermediate_parameters.toml.tpl') as infile, open('pest_intermediate_parameters.toml', 'w') as outfile:
    for line in infile:
        if "ptf" in line:
            continue
        for src, target in replacements.items():
            line = line.replace(f"{src}", str(target))
        outfile.write(line)