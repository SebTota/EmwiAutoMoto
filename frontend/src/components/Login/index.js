import React from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import {login} from "../../controllers/userController"

import "./styles.css"

export default function Login(props) {
    const [showWrongPasswordAlert, setShowPasswordAlert] = React.useState(false);


    function loginHandler() {
        setShowPasswordAlert(false);
        const username = document.getElementById("formGroupEmail").value;
        const password = document.getElementById("formGroupPassword").value;

        login(username, password).then((data) => {
            localStorage.setItem('emwi-auto-moto-access-token', data['access_token']);
            window.location.href = '/';
        }).catch((err) => {
            setShowPasswordAlert(true);
        })
    }

    let passwordAlert;
    if (showWrongPasswordAlert) {
        passwordAlert = <Alert className="m-3" key="warning" variant="warning">Wrong password. Please try again.</Alert>
    }

    return (
        <div className="loginWrapper">
            <Form>
                <Form.Group className="mb-3" controlId="formGroupEmail">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control type="email" placeholder="Enter email"/>
                </Form.Group>
                <Form.Group className="mb-3" controlId="formGroupPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Password"/>
                </Form.Group>
                <Button variant="primary" onClick={() => {loginHandler()}}>Save</Button>
                {passwordAlert}
            </Form>
        </div>
    )
}
