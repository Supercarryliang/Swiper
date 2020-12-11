import pymysql as pymysql

from libs.orm import patch_model

pymysql.install_as_MySQLdb()



#在django的model加载前,加载打补丁之后的model
patch_model()