import xmlrpc.client
from os import system
from tabulate import tabulate
import base64

system("cls")
# ------------------------------------------------------------------------------------------------------------------------------

url = ""
db = ""
username = ''
password = ""


common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
print(common.version())

uid = common.authenticate(db, username, password, {})
print(uid)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


# id = models.execute_kw(db, uid, password, 'hr.job', 'create', [
#                        {'name': "hello world world"}])
