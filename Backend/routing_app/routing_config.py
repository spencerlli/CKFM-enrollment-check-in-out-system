import os

if os.path.exists('/.dockerenv'):    # running in docker
    REST_API = 'http://restful_api:5001'
else:
    REST_API = 'http://localhost:5001'

DEFAULT_PWD = '123456'
