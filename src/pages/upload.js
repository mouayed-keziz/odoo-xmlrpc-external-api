import axios from 'axios';
import { useState } from 'react';

const FileUploader = () => {

    const [partner_name, setPartner_name] = useState("mouayed")
    const [email, setEmail] = useState("mouayed@admin.dev")
    const [phone, setPhone] = useState("07 77 77 77 77")
    const [files, setFiles] = useState([]);

    const handleFileChange = (event) => {
        if (!event.target.files.length) return;
        const files = Array.from(event.target.files);
        const readerPromises = files.map((file) => {
            return new Promise((resolve) => {
                const reader = new FileReader();
                reader.onload = () => {
                    const content = reader.result.split(',')[1]; // Extract base64 content
                    resolve({
                        name: file.name,
                        datas: content,
                        res_model: "hr.applicant"
                    });
                };
                reader.readAsDataURL(file);
            });
        });

        Promise.all(readerPromises).then((contents) => {
            setFiles(contents);
        });
    };

    const handleButtonClick = async () => {
        const result = await axios.post("/api/upload", { files, partner_name, email, phone })
        console.log(result.data)
    };

    const classes =
        "focus:outline-none text-white bg-purple-700 hover:bg-red-100 focus:ring-4 focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:bg-red-800 dark:hover:bg-red-900 dark:focus:ring-black-900";

    return (
        <div className="w-screen h-screen flex justify-center items-center flex-col">
            <input
                className={classes}
                type="text"
                placeholder="partner-name"
                value={partner_name}
                onChange={(e) => setPartner_name(e.target.value)}
            />
            <input
                className={classes}
                type="email"
                placeholder="mouayed@admin.dev"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <input
                className={classes}
                type="text"
                placeholder="07 77 77 77 77"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
            />
            <input
                className={classes}
                type="file"
                multiple
                onChange={handleFileChange}
            />
            <button className={classes} onClick={handleButtonClick}>
                Log File Content
            </button>
        </div>
    );
};

export default FileUploader;