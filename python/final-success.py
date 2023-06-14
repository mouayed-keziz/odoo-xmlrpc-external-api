import xmlrpc.client
from os import system
from tabulate import tabulate
import base64


# ------------------------------------------------------------------------------------------------------------------------------

url = ""
db = ""
username = ""
password = ""


common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
# url, db, username, password = info['host'], info['database'], info['user'], info['password']
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
id = models.execute_kw(db, uid, password, 'hr.job', 'create', [
                       {'name': "hello world world"}])

# ------------------------------------------------------------------------------------------------------------------------------


def get_all_job_applications():
    applications = models.execute_kw(db, uid, password, 'hr.applicant', 'search_read', [], {'fields': [
                                     'partner_name', 'job_id', 'name', 'email_from', 'type_id', 'partner_phone', "stage_id", "attachment_number", "attachment_ids"]})
    list_to_be_printed = []
    for application in applications:
        list_to_be_printed.append([application['partner_name'], application['job_id'], application['name'], application['email_from'],
                                   application['type_id'], application['partner_phone'], application["stage_id"], application["attachment_number"], application["attachment_ids"]])
    print(tabulate(list_to_be_printed, headers=[
          'partner_name', 'job_id', 'name', 'email_from', 'type_id', 'partner_phone', 'stage_id', "attachment_number", "attachment_ids"]))
# ------------------------------------------------------------------------------------------------------------------------------


def create_job_application(job_id, name, partner_name, email, phone, file_path, type_id):
    # Create attachment
    with open(file_path, 'rb') as file:
        file_data = file.read()

    attachment_data = {
        'name': file_path.split('/')[-1],
        'datas': base64.b64encode(file_data).decode('utf-8'),
        'res_model': 'hr.applicant',
    }
    

    attachment_id = models.execute_kw(
        db, uid, password, 'ir.attachment', 'create', [attachment_data]
    )

    # Create job application
    application_data = {
        'name': name,
        "partner_name": partner_name,
        'email_from': email,
        'partner_phone': phone,
        'job_id': job_id,
        "type_id": type_id,
        'attachment_ids': [(6, 0, [attachment_id])],
    }

    application_id = models.execute_kw(
        db, uid, password, 'hr.applicant', 'create', [application_data]
    )

    print(f"New Job Application ID: {application_id}")
# ------------------------------------------------------------------------------------------------------------------------------


system("cls")
# Example usage
job_id = 7
name = "THL BDD MD RO"
partner_name = "John Doe"
email = "johndoe@example.com"
phone = "123456789"
file_path = "ai_in_securdity.pdf"
type_id = 1
create_job_application(job_id, name, partner_name,
                       email, phone, file_path, type_id)
get_all_job_applications()
