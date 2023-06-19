import create_job_application from "@/odoo";
import formidable from "formidable";
import z from "zod";

const handeler = async (req, res) => {
    const form = new formidable.IncomingForm({ multiples: true });

    const formData = new Promise((resolve, reject) => {
        form.parse(req, async (err, fields, files) => {
            if (err) {
                reject("error");
            }
            resolve({ fields, files });
        });
    });

    let { fields } = await formData;

    const schema = z.object({
        partner_name: z.string(),
        email: z.string().email(),
        phone: z.string(),
        files: z.array(z.object({
            name: z.string(),
            datas: z.string(),
            res_model: z.string(),
        })),
    });

    try {
        fields = schema.parse(fields);
    } catch (error) {
        res.status(200).send({ error: error.errors });
    }

    const partener_id = await create_job_application({
        partner_name: "mouayed keziz",
        email: "mouayed@admin.dev",
        phone: "07 77 77 77 77",
        files: fields.files,
    });

    res.send({ partener_id });
}


export const config = {
    api: {
        bodyParser: false,
    }
}

export default handeler;