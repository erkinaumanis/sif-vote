import os
import urllib
import urllib2
import json
import pdb
import datetime
from optparse import OptionParser

from app import *

#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":
    from app import config
    
    # environment configuration
    parser = OptionParser()
    parser.add_option("--test", action="store_true", dest="test_mode") 
    parser.add_option("--prod", action="store_true", dest="prod_mode")

    (options,args) = parser.parse_args()

    app = None
    if options.test_mode:
        app = start_app(config.Test)
    elif options.prod_mode:
        app = start_app(config.Prod)
    else:
        app = start_app(config.Dev)

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

