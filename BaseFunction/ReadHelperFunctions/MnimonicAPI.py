def read_mnemonic(text: str):
    text_list = text.split('\n')
    well_names = []
    num_names = []
    values = []
    for line in text_list:
        if 'WELL' in line.upper():
            well_name = line.upper().split(':')[1]
            well_name = well_name.split(',')[0].strip().replace("'", '')
            well_names.append(well_name)
            num_name = line.upper().split(':')[-2]
            num_name = int(num_name.strip().replace("'", ''))
            num_names.append(num_name)
        elif line.upper() != '':
            values.append(float(line.strip()))
    if len(well_names) == len(num_names) and len(num_names) == len(values):
        return well_names, num_names, values