import xmlrpc.client
import base64
from os import system
from tabulate import tabulate

system("cls")
# ------------------------------------------------------------------------------------------------------------------------------

url = "https://test.test-test.net"
db = "test"
username = 'admin'
password = "test"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
print("logged in : ", uid)

# ------------------------------------------------------------------------------------------------------------------------------


def all_jobs_with_id():
    jobs = models.execute_kw(db, uid, password, 'hr.job', 'search_read', [
                             []], {'fields': ['id', 'name', 'display_name', 'description']})
    list_to_be_printed = []
    for job in jobs:
        list_to_be_printed.append(
            [job['id'], job['name'], job['display_name'], job["description"]])
    print(tabulate(list_to_be_printed, headers=[
        "ID", "Name", "Display Name", "description"]))


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


# EXAMPLE :
job_id = 11
name = "developer"
partner_name = "test test"
email = "dev@example.com"
phone = "123456789"
file_path = "testpdf.pdf"
type_id = 1
create_job_application(job_id, name, partner_name,
                       email, phone, file_path, type_id)
all_jobs_with_id()


# ------------------------------------------------------------------------------------------------------------------------------
# 11 * Chargé d'affaire
# ------------------------------------------------------------------------------------------------------------------------------
