#! /home/melissa/my_environments/py3SQLAlchemyEnv/bin/python
from config import app
import routes

if __name__ == "__main__":
  app.run(host="0.0.0.0",port="80",debug = True)
