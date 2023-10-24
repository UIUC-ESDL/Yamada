"""
This script converts all notebooks in the test directories to scripts.

PyTest does not recognize notebooks. However, notebooks are useful for explaining the logic and visuals of scientific
computing test cases.
"""

import subprocess

test_directory_1 = "test_spatial_graphs"
test_directory_2 = "test_yamada"
test_directory_3 = "test_spatial_graph_diagrams"
test_directories = [test_directory_1, test_directory_2, test_directory_3]

cd_commands = ["cd " + test_directory + " && " for test_directory in test_directories]

nb_command = ["jupyter nbconvert --output-dir=", " --to python *.ipynb"]

output_directories = ['../test_notebook_to_script_conversion', '../test_notebook_to_script_conversion','../test_notebook_to_script_conversion']

for cd_command, output_directory in zip(cd_commands, output_directories):
    subprocess.run(cd_command + nb_command[0] + output_directory + nb_command[1], shell=True, check=True)
