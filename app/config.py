class Config(object):

  # use debug mode?
  DEBUG = True

  # use testing mode?
  TESTING = False

  # database configuration
  MONGODB_DB = "sif-vote"
  MONGODB_HOST = "ds053178.mongolab.com:53178/sif-vote"

class Test(Config):

  # use testing mode?
  TESTING = True

  # database configuration
  MONGODB_DB = "test-sif-vote"
  MONGODB_HOST = "ds027789.mongolab.com:27789/test-sif-vote"

class Prod(Config):
  DEBUG = False

class Dev(Config):
  pass