import sys
path='e:/Pythonweb/py344/project_code/fernando'
if path not in sys.path:
    sys.path.insert(0, path)
from index import app as application