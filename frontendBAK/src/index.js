import React from 'react';
import ReactDOM from 'react-dom/client';
import {BrowserRouter, Routes, Route} from "react-router-dom";

import App from './App';
import MotorcycleRoute from "./routes/motorcycleRoute";
import EditMotorcycleRoute from "./routes/editMotorcycleRoute"
import LoginRoute from "./routes/loginRoute"
import {PrivateRoute} from "./routes/PrivateRoute";
import reportWebVitals from './reportWebVitals';
import $ from "jquery";
import 'bootstrap/dist/css/bootstrap.min.css';

import './index.css';
import HeaderNavbar from "./components/Navbar/navbar";


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <BrowserRouter>
            <HeaderNavbar/>
            <Routes>
                <Route path="/" element={<App/>}/>
                <Route path="/motorcycle">
                    <Route path=":id" element={<MotorcycleRoute/>}/>
                </Route>
                <Route path="/motorcycle/edit">
                    <PrivateRoute path=":id" components={}
                    <Route path=":id" element={<PrivateRoute><EditMotorcycleRoute type='edit'/></PrivateRoute>}/>
                </Route>
                <Route path="/motorcycle/new" element={<PrivateRoute><EditMotorcycleRoute type='new'/></PrivateRoute>}/>
                <Route path="/login" element={<LoginRoute/>}/>
                <Route
                    path="*"
                    element={
                        <main style={{padding: "1rem"}}>
                            <p>There's nothing here!</p>
                        </main>
                    }
                />
            </Routes>
        </BrowserRouter>
    </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
