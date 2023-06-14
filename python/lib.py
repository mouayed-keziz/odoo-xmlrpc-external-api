import mimetypes
import xmlrpc.client
from os import system
from tabulate import tabulate
import base64

# ------------------------------------------------------------------------------------------------------------------------------

info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
url, db, username, password = info['host'], info['database'], info['user'], info['password']
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
id = models.execute_kw(db, uid, password, 'hr.job', 'create', [
                       {'name': "hello world world"}])

# ------------------------------------------------------------------------------------------------------------------------------


def all_jobs_with_id():
    jobs = models.execute_kw(db, uid, password, 'hr.job', 'search_read', [
                             []], {'fields': ['id', 'name']})
    for job in jobs:
        job_id = job['id']
        job_name = job['name']
        print(f"Job ID: {job_id}, Job Name: {job_name}")

# ------------------------------------------------------------------------------------------------------------------------------


def get_job_applications_from_job_id(job_id):
    applications = models.execute_kw(db, uid, password, 'hr.applicant', 'search_read', [[('job_id', '=', job_id)]], {
                                     'fields': ['employee_name', 'job_id', 'name', 'email_from', 'type_id', 'partner_phone', "stage_id", ]})
    list_to_be_printed = []
    for application in applications:
        list_to_be_printed.append([application['employee_name'], application['job_id'], application['name'], application['email_from'],
                                   application['type_id'], application['partner_phone'], application["stage_id"]])
    print(tabulate(list_to_be_printed, headers=[
          'employee_name', 'job_id', 'name', 'email_from', 'type_id', 'partner_phone', 'stage_id']))


# ------------------------------------------------------------------------------------------------------------------------------

def get_all_job_applications():
    applications = models.execute_kw(db, uid, password, 'hr.applicant', 'search_read', [], {'fields': [
                                     'employee_name', 'job_id', 'name', 'email_from', 'type_id', 'partner_phone', "stage_id", "attachment_number", "attachment_ids"]})
    list_to_be_printed = []
    for application in applications:
        list_to_be_printed.append([application['employee_name'], application['job_id'], application['name'], application['email_from'],
                                   application['type_id'], application['partner_phone'], application["stage_id"], application["attachment_number"], application["attachment_ids"]])
    print(tabulate(list_to_be_printed, headers=[
          'employee_name', 'job_id', 'name', 'email_from', 'type_id', 'partner_phone', 'stage_id', "attachment_number", "attachment_ids"]))
# ------------------------------------------------------------------------------------------------------------------------------


def get_attrubites_of(model_name):
    model_fields = models.execute_kw(db, uid, password, model_name, 'fields_get', [
    ], {'attributes': ['string', 'type']})

    list_to_be_printed = []
    for field_name, field_attrs in model_fields.items():
        field_label = field_attrs['string']
        field_type = field_attrs['type']
        list_to_be_printed.append([field_name, field_label, field_type])
    print(tabulate(list_to_be_printed, headers=[
          'field name', 'field label', 'field type']))

# ------------------------------------------------------------------------------------------------------------------------------


def get_all_models():
    model_list = models.execute_kw(db, uid, password, 'ir.model', 'search_read', [
                                   []], {'fields': ['model', 'name']})
    list_to_be_printed = []
    for model in model_list:
        model_name = model['model']
        model_display_name = model['name']
        list_to_be_printed.append([model_name, model_display_name])
    with open("models.txt", "w") as f:
        f.write(tabulate(list_to_be_printed, headers=[
            'model_name', 'model_display_name']))

# ------------------------------------------------------------------------------------------------------------------------------


def add_job_application(job_id, name, employee_name, email_from, partner_phone):
    new_application_data = {
        "name": name,
        'employee_name': employee_name,
        'email_from': email_from,
        'partner_phone': partner_phone,
        'job_id': job_id,
        'type_id': 1,
        'stage_id': 3,
        'categ_ids': [1, 2],
        # Add additional fields as required
    }
    new_application_id = models.execute_kw(
        db, uid, password, 'hr.applicant', 'create', [new_application_data])
    print(f"New Application ID: {new_application_id}")
# ------------------------------------------------------------------------------------------------------------------------------


def get_attachements_of_somebody():
    # get applications with (attachement number, and attachement id)
    applications = models.execute_kw(db, uid, password, 'hr.applicant', 'search_read', [[('job_id', '=', 7)]], {'fields': [
                                     'employee_name', 'job_id', 'name', 'email_from', 'type_id', 'partner_phone', "attachment_number", "attachment_ids"]})

    # third application has 1 attachement (so first), we take the id of that attachement
    attachment_id = applications[2]['attachment_ids'][0]

    # get the name and the binary data of the attachement
    attachment_data = models.execute_kw(db, uid, password, 'ir.attachment', 'read', [
        attachment_id], {'fields': ['name', 'datas']})

    # extract the name and the binary data of the attachement
    attachment_name = attachment_data[0]['name']
    attachment_datas = attachment_data[0]['datas']

    # decode the binary data
    with open(attachment_name, 'wb') as file:
        file.write(base64.b64decode(attachment_datas))

# ------------------------------------------------------------------------------------------------------------------------------


def create_attachment(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    attachment_data = {
        # Extracting the file name from the path
        'name': file_path.split('/')[-1],
        'datas': base64.b64encode(file_data).decode('utf-8'),
    }
    attachment_id = models.execute_kw(
        db, uid, password, 'ir.attachment', 'create', [attachment_data]
    )
    print(f"New Attachment ID: {attachment_id}")
    myList = []
    myList.append(attachment_id)
    return myList


def create_job_application(job_id, name, email, phone, attachment_ids=None):
    print("attachment_ids", attachment_ids)
    new_application_data = {
        'name': name,
        'email_from': email,
        'partner_phone': phone,
        'job_id': job_id,
        "attachment_number": len(attachment_ids) if attachment_ids else 0,
        'attachment_ids': attachment_ids,
        # Add additional fields as required
    }
    new_application_id = models.execute_kw(
        db, uid, password, 'hr.applicant', 'create', [new_application_data]
    )
    print(f"New Application ID: {new_application_id}")


system("cls")
attachment_path = 'testpdf.pdf'
attachment_id = create_attachment(attachment_path)
create_job_application(7, "anum anum", "testanum@anum.dev",
                       "123456789", attachment_ids=attachment_id)
get_all_job_applications()
