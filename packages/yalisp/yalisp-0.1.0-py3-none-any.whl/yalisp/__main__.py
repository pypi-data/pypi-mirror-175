import sys
import yaml
from .lisp import interpriter


interpriter.execute(yaml.load(
    open(sys.argv[1], 'r').read().expandtabs(2),
    Loader=yaml.FullLoader
))
