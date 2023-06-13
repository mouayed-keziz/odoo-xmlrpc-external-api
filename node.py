import xmlrpc.client
import base64

url = "https://erp.testtest.net"
db = "testtest"
username = 'admin'
password = "testtest"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


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


job_id = 11
name = "developer"
partner_name = "test test"
email = "dev@example.com"
phone = "123456789"
file_path = "testpdf.pdf"
type_id = 1
create_job_application(job_id, name, partner_name,
                       email, phone, file_path, type_id)
