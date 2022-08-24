import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import App from './App';
import MotorcycleRoute from "./routes/motorcycleRoute";
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.min.css';

import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <div className="wrapper">
        <React.StrictMode>
          <BrowserRouter>
              <Routes>
                  <Route path="/" element={<App />} />
                  <Route path="motorcycle" >
                      <Route path=":id" element={<MotorcycleRoute />} />
                  </Route>
                  <Route
                      path="*"
                      element={
                        <main style={{ padding: "1rem" }}>
                          <p>There's nothing here!</p>
                        </main>
                      }
                    />
              </Routes>
          </BrowserRouter>
      </React.StrictMode>
    </div>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
