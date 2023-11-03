import React, { useEffect, useState } from 'react';
import {createRoot} from 'react-dom/client'
import '../assets/tailwind.css'
import './popup.css'

const handleInput = (e) => {
    e.preventDefault();
    const name = e.target[0].value
    chrome.storage.sync.set({name}, () => {
        console.log(`name is set to ${name}`)
    });
}

const Popup = () => {
    useEffect(() => {
        chrome.storage.sync.get(["name"], (res) => {
            console.log(res.name)
        })
    }, [])

    return (
    <div className='h-screen'>
        <form onSubmit={handleInput} className="flex justify-center items-center py-44">
            <input type="text" name = "name" className='bg-gray ring-black px-4 py-4' placeholder="Enter a word"/>
            <button className="py-4 px-3 bg-indigo-500 text-white m-2">Submit</button>

        </form>    
    </div>
    );
}

export default Popup;