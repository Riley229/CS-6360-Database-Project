import React from 'react';
import { useState } from 'react';
import { GiSoccerBall } from "react-icons/gi";
import { GiSoccerField } from "react-icons/gi";
import { IoMenu } from "react-icons/io5";

const SideNav = () => {
  
  const [side, setSide] = useState(true);

  const setSideVal = () => {
    setSide(!side);
  }

  return (
    <div>
        <div onClick={setSideVal} className='cursor-pointer fixed right-5 top-5 sm:right-10 sm:top-10'>
            <IoMenu size={35}/>
        </div>
        <div className={side ? 'fixed w-[70px] h-full bg-[#0d406ae3] ease-in duration-500' :
         ' fixed left-[-100%] top-0 ease-in duration-300'}>
            <a href='#hero'>
                <div className='flex items-end tracking-widest font_logo'>
                    <h1 className='text-6xl ml-[14px] text-white'>S</h1>
                    <h2 className='text-4xl text-[#042138e3]'><span className='text-white mr-[3px]'>o</span>ccer</h2>
                </div>
                <div className='flex items-end tracking-widest font_logo'>
                    <h1 className='text-6xl ml-[29px] text-white'>P</h1>
                    <h2 className='text-4xl ml-[3px] text-[#042138e3]'>redict</h2>
                </div>
            </a>
            <div className='w-[50px] mx-auto h-[60%] flex flex-col items-center justify-center'>
                <a href="#hero" >
                    <div className='tooltip my-[60px]'>
                        <GiSoccerBall className=' text-white' size={40}/>
                        <span className='tooltip-text px-2'>Home</span>
                    </div>
                </a>
                <a href="#hist">
                    <div className='tooltip'>
                        <GiSoccerField className='text-white' size={40}/>
                        <span className='tooltip-text px-2'>History</span>
                    </div>
                </a>
            </div>
        </div>
    </div>
  )
}

export default SideNav