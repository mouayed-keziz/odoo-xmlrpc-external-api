import Image from 'next/image'
import { Inter } from 'next/font/google'
import { useForm } from '@mantine/form';

const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  const form = useForm({
    initialValues: {
      name: 'mouayed',
      email: 'mouayed@admin.dev',
      phone: '07 77 77 77 77',
      description: 'this is a description of the job application test',
      file: null
    },
  });

  const submitHandeler = async (values) => {
    const formData = new FormData();
    formData.append('name', form.values.name);
    formData.append('email', form.values.email);
    formData.append('phone', form.values.phone);
    formData.append('description', form.values.description);
    formData.append('file', form.values.file);
  }

  // card has shadow, radius , padding and a small border
  const card = "shadow-md rounded-md p-10 border border-gray-200"
  return (
    <>
      <div className='w-screen h-screen flex flex-col justify-center items-center '>
        <form
          className='shadow-md rounded-md px-10 py-4 border border-gray-200'
          onSubmit={form.onSubmit((values) => submitHandeler(values))}
        >

          {/* name input section */}
          <div className='flex justify-start items-center gap-4 my-4' >
            <label>name :</label  >
            <input
              type='text' className='border border-gray-200 rounded-md p-2'
              {...form.getInputProps('name')}
            />
          </div>

          {/* email input section */}
          <div className='flex justify-start items-center gap-4 my-4' >
            <label>email :</label>
            <input
              type='text' className='border border-gray-200 rounded-md p-2'
              {...form.getInputProps('email')}
            />
          </div>

          {/* phone input section */}
          <div className='flex justify-start items-center gap-4 my-4' >
            <label>phone :</label>
            <input
              type='text' className='border border-gray-200 rounded-md p-2'
              {...form.getInputProps('phone')}
            />
          </div>

          {/* description input section */}
          <div className='flex justify-start items-center gap-4 my-4' >
            <label>description :</label>
            <input
              type='text' className='border border-gray-200 rounded-md p-2'
              {...form.getInputProps('description')}
            />
          </div>

          <div className='flex justify-start items-center gap-4 my-4' >
            <label>description :</label>
            <input
              type='file' className='border border-gray-200 rounded-md p-2'
              onChange={(e) => form.setFieldValue('file', e.target.files[0])}
            />
          </div>

          <div className='w-full flex justify-center items-center gap-4' >
            <button
              className='focus:outline-none text-white bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-900'
              type='submit'
            >press</button>

            <button
              className='focus:outline-none text-white bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-900'
              onClick={() => console.log(form.values.file)}
            >log</button>
          </div>

        </form>
      </div>

    </>
  )
}

