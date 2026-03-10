try:
    import pathlib
    import toml
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "toml"])
    import toml
file = pathlib.Path(__file__).parent
while not 'config.txt' in file.iterdir():
    file = file.parent
def write_to_config(key, new):
    global file
    with open(file, 'r+') as f:
        thing = f.read()
        thing = toml.loads(thing)
        thing[key] = new
        f.write(toml.dumps(thing))
def read_from_config(key):
    global file
    with open(file, 'r+') as f:
        thing = f.read()
        thing = toml.loads(thing)
        f.write(thing.get(key, None))
def get_config(key):
    global file
    with open(file, 'r+') as f:
        return toml.loads(f.read())
if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'set':
        write_to_config(sys.argv[2], sys.argv[3])
    elif sys.argv[2] == 'read':
        read_from_config(sys.argv[2])
    elif sys.argv[2] == 'view':
        print(get_config)
    else:
        print('Usage: \\mscfgutil <set|read|view>')
