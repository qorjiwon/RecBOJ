import React from "react";
import {Routes, Route} from 'react-router-dom'
import Home from './components/Home'
import About from './components/About'



function Tabs() {
    return (
        <div>
            <ul>
                <li>
                    <a href="#/">Home</a>
                </li>
                <li>
                    <a href ="#/about">About</a>
                </li>
            </ul>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route index element={<About />} />
            </Routes>
        </div>
    )
}

export default Tabs