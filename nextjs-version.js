const Odoo = require('async-odoo-xmlrpc');
const fs = require("fs")
const path = require('path');
require("dotenv").config({ path: path.join(__dirname, "./env/.env") });
console.clear()


const odoo_config = {
    url: process.env.ODOO_URL,
    db: process.env.ODOO_DB,
    username: process.env.ODOO_USERNAME,
    password: process.env.ODOO_PASSWORD,
}

var odoo = new Odoo(odoo_config);



async function create_job_application(name, partner_name, email, phone, job_id, type_id, file_path) {

    await odoo.connect();
    console.table(odoo_config)

    const application_data = {
        'name': name,
        "partner_name": partner_name,
        'email_from': email,
        'partner_phone': phone,
        'job_id': job_id,
        "type_id": type_id,
    }
    var application_id = undefined

    try {
        application_id = await odoo.execute_kw(
            'hr.applicant', 'create', [application_data]
        )
    } catch (error) {
        console.log("Error while creating application 1")
        exit()
    }

    for (let index = 0; index < file_path.length; index++) {
        const file = file_path[index];
        const fileData = await fs.promises.readFile(file);
        const attachmentData = {
            name: path.basename(file),
            datas: fileData.toString('base64'),
            res_model: 'hr.applicant'
        };
        var attachement_id = undefined
        try {
            attachement_id = await odoo.execute_kw('ir.attachment', 'create', [attachmentData])
        } catch (error) {
            console.log("Error while creating attachement 2")
            continue
        }

        var updated_application_id = undefined
        try {
            updated_application_id = await odoo.execute_kw("hr.applicant", "write", [[application_id], { "attachment_ids": [[4, attachement_id]] }])
        } catch (error) {
            console.log("Error while updating application 3")
            continue
        }
    }
}

const job_id = 11
const name = "4fun"
const partner_name = "4fun"
const email = "4fun@gmail.com"
const phone = "123456789"
const type_id = 1
const file_path = []
// const file_path = ["./files/test.png", "./files/test.pdf", "./files/test3.png"]

create_job_application(name, partner_name, email, phone, job_id, type_id, file_path)