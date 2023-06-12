import xmlrpc.client
import os

os.system("cls")

info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
url, db, username, password = info['host'], info['database'], info['user'], info['password']

print("URL: ", url)
print("DB: ", db)
print("Username: ", username)
print("Password: ", password)

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()

uid = common.authenticate(db, username, password, {})

print(uid)
