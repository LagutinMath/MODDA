import json
import os

try:
    with open('resources/paths.json') as file:
        paths = json.load(file)
except Exception as e:
    print(e)
    paths = {}

pwd = os.getcwd()
resource_dir = os.path.abspath(paths.get('resource_dir', pwd))
des_dir = os.path.abspath(paths.get('des_dir', pwd))
meas_dir = os.path.abspath(paths.get('meas_dir', pwd))

if __name__ == '__main__':
    print(pwd)
    print(resource_dir)
    print(des_dir)
    print(meas_dir)
