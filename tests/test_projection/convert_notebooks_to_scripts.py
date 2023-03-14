import subprocess

subprocess.run("jupyter nbconvert --to python *.ipynb", shell=True, check=True)