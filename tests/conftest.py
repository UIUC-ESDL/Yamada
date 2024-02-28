import os
import subprocess

def pytest_sessionstart(session):


    test_directory = os.path.join(os.getcwd(), 'tests')
    output_directory = os.path.join(test_directory, 'test_notebook_to_script_conversion')

    # Empty the output directory of Python scripts, except __init__.py
    for item in os.listdir(output_directory):
        item_path = os.path.join(output_directory, item)
        if item.endswith(".py") and item != "__init__.py":
            os.remove(item_path)

    # Get the filepaths of all notebooks in the test directory and its subdirectories
    filepaths = []
    for dirpath, dirnames, filenames in os.walk(test_directory):
        filepaths += [os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.ipynb')]

    # Convert the notebooks to scripts
    for filepath in filepaths:
        nb_command = ["jupyter", "nbconvert", "--output-dir=" + output_directory, "--to", "python", filepath]
        try:
            result = subprocess.run(nb_command, check=True, capture_output=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error converting:", filepath)
            print(e.stderr.decode())

    print('Conversion Done!')
