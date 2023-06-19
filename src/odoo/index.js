import Odoo from "odoo-await"


async function create_job_application({ partner_name, email, phone, files }) {
    const odoo_config = {
        baseUrl: process.env.ODOO_URL,
        db: process.env.ODOO_DB,
        username: process.env.ODOO_USERNAME,
        password: process.env.ODOO_PASSWORD
    }

    const odoo = new Odoo(odoo_config)
    await odoo.connect()

    const job_application_data = {
        name: process.env.ODOO_JOB_NAME,
        partner_name: partner_name,
        email_from: email,
        partner_phone: phone,
        job_id: process.env.ODOO_JOB_ID,
        type_id: process.env.ODOO_TYPE_ID,
        attachment_ids: files.map((file) => {
            return [0, 0, {
                name: file.name,
                datas: file.datas,
                res_model: file.res_model,
            }]
        }
        )
    }
    const partnerId = await odoo.create('hr.applicant', job_application_data);
    return partnerId;
}

export default create_job_application;