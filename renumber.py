import re
import shutil

def renumber_classes(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    pattern = re.compile(r'class Level(\d+)')
    pattern2 = re.compile(r'max_level = (\d+)')
    last_level_number = 0
    start_renumbering = False

    for i, line in enumerate(lines):
        match = pattern.match(line.strip())
        match2 = pattern2.match(line.strip())
        if match:
            level_number = int(match.group(1))
            if level_number <= last_level_number:
                offset = last_level_number - level_number + 1
                start_renumbering = True

            if start_renumbering:
                new_level_number = level_number + offset
                lines[i] = line.replace(f'Level{level_number}', f'Level{new_level_number}')
                last_level_number = new_level_number
            else:
                last_level_number = level_number

        if match2:
            lines[i] = line.replace(f'{match2.group(1)}', f'{new_level_number}')

    with open(filename, 'w') as file:
        file.writelines(lines)

# Usage
filename = 'levels.py'
bkup = 'levels.py.bkup'  # will overwrite so check before rerun script
shutil.copy(filename, bkup)
renumber_classes(filename)
