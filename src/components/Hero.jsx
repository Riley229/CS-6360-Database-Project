import React from 'react'

const Hero = () => {
  return (
    <div id="hero" className='w-full h-screen flex items-center'>
        <div className='max-w-[1240px] mx-auto p-1'>
            <div className='mb-[100px]'>
                <h2 className='text-center text-[#042138e3]'>Welcome to Soccer Predict</h2>
                <p className='text-gray-400 text-center uppercase pt-2 tracking-wider'>A platform to predict the score of incoming soccer matches</p>
            </div>
            <div className='max-w-[1050px] mx-auto'>
                <h3 className='text-[#042138e3]'>Let's Predict</h3>
                <p className='text-gray-500 text-sm tracking-wider'>Enter the information about the match you want to predict</p>
                <div className='mt-[25px]'>
                    <form action="">
                        <div className='grid grid-cols-3 gap-8'>
                            <div className='flex flex-col'>
                                <label className='text-[#042138e3] text-lg' for='home_team'>Home Team</label>
                                <input className='text-[#021321e3] px-2 h-[45px] rounded-lg border-gray-300 border-[2px] focus:outline-[2px] outline-gray-400' id='home_team' type='text' name='home_team'/>
                            </div>
                            <div className='flex flex-col'>
                                <label className='text-[#042138e3] text-lg' for='away_team'>Away Team</label>
                                <input className='text-[#021321e3] px-2 h-[45px] rounded-lg border-gray-300 border-[2px] focus:outline-[2px] outline-gray-400' id='away_team' type='text' name='away_team'/>
                            </div>
                            <div className='flex flex-col'>
                                <label className='text-[#042138e3] text-lg' for='date'>Date</label>
                                <input className='text-[#021321e3] px-2 h-[45px] rounded-lg border-gray-300 border-[2px] focus:outline-[2px] outline-gray-400' id='date' type='date' name='date'/>
                            </div>

                            <div></div>
                            <div className='mx-auto '>
                                <button className='rounded-lg text-lg bg-[#0d406ae3] text-white border-2 border-[#0d406a] h-[45px] w-[100px] sm:w-[200px] flex justify-center items-center'>Submit</button>
                            </div>
                            <div></div>
                        </div>
                    </form>
                </div>

                <div className='mt-[50px]'>
                    <div className='p-2 h-[140px] max-w-[1050px] mx-auto shadow-md shadow-gray-300 rounded-lg flex items-center justify-between'>
                        <div className='sm:ml-[85px] h-[50px] border-2 p-2 bg-gray-100 rounded-xl'>
                            <p className='text-[#042138e3]'>Home_Team_Name</p>
                        </div>
                        <div className='text-[#042138e3]'>
                            <h2 className='text-4xl font-medium'>1</h2>
                        </div>
                        <div className='text-[#042138e3]'>
                            <h2 className='font_cursive text-4xl font-medium'>vs</h2>
                        </div>
                        <div className='text-[#042138e3]'>
                            <h2 className='text-4xl font-medium'>0</h2>
                        </div>
                        <div className='sm:mr-[85px] h-[50px] border-2 p-2 bg-gray-100 rounded-xl'>
                            <p className='text-[#042138e3]'>Away_Team_Name</p>
                        </div>
                    </div>
                </div>

                <div className='mt-[35px]'>
                    <a href='#hist'>
                        <p className='border-2 border-[#0d406a] inline p-[6px] text-[14px] rounded-lg text-white bg-[#0d406ae3]'>Last Five Predictions</p>
                    </a>
                </div>
            </div>
        </div>
    </div>
  )
}

export default Hero