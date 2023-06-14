const Odoo = require('async-odoo-xmlrpc');
const fs = require("fs")
const path = require('path');
const { exit } = require('process');
require("dotenv").config({ path: path.join(__dirname, "./env/.env") });
console.clear()

const odoo_config = {
    url: process.env.ODOO_URL,
    //port: undefined,
    db: process.env.ODOO_DB,
    username: process.env.ODOO_USERNAME,
    password: process.env.ODOO_PASSWORD,
}

var odoo = new Odoo(odoo_config);

async function get_application_by_email(email) {
    await odoo.connect();
    console.table(odoo_config)

    const application = await odoo.execute_kw('hr.applicant', "search_read", [[["email_from", "=", email]]])
    console.log(application)

}

async function get_attachement_by_id(id) {
    await odoo.connect();
    console.table(odoo_config)

    const attachement = await odoo.execute_kw('ir.attachment', "search_read", [[["id", "=", id]]])
    //write attachement to json file
    fs.writeFileSync("attachement.json", JSON.stringify(attachement, null, 2))
}

async function DeleteJob(job_id) {
    await odoo.connect();
    console.table(odoo_config)

    let result = undefined
    try {
        result = await odoo.execute_kw('hr.job', "unlink", [[job_id]])
    } catch (error) {
        console.log("Error while deleting job")
        exit()
    }
}

async function Main() {
    await odoo.connect();
    console.table(odoo_config)
    console.log(odoo)
    const jobs = await odoo.execute_kw('hr.job', "search_read", [])
    console.log(jobs.map(job => ({ id: job.id, name: job.name })))
}


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
const name = "test4"
const partner_name = "4-test with 3 files (middle is corrupted)"
const email = "test4@test.com"
const phone = "444444444"
const type_id = 1
const file_path = ["./files/test.png", "./files/test.pdf", "./files/test3.png"]
//const file_path = ["./files/test.png"]


//Main();
create_job_application(name, partner_name, email, phone, job_id, type_id, file_path)



// get_application_by_email("athmanimanel@gmail.com")

// get_attachement_by_id(7076)
