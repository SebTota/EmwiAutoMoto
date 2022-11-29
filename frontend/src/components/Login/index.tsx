import React, {useState} from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import {login} from "../../controllers/tsUserController"

import "./styles.css"

export default function Login(props: any) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showWrongPasswordAlert, setShowPasswordAlert] = React.useState(false);


    function loginHandler(event: any) {
        event.preventDefault();
        setShowPasswordAlert(false);

        login(username, password).then((data) => {
            console.log("yay! We're signed in. Auth: ", data);
            console.log(data);
            // localStorage.setItem('emwi-auto-moto-access-token', data['access_token']);
            // localStorage.setItem('emwi-auto-moto-username', data['username']);
            // window.location.href = '/';
        }).catch((err) => {
            console.log("Uh oh.", err)
            setShowPasswordAlert(true);
        })
    }

    let passwordAlert;
    if (showWrongPasswordAlert) {
        passwordAlert = (<Alert className="m-3" key="warning" variant="warning">Wrong password. Please try again.</Alert>);
    }

    function handleUsernameInput(event: any) {
        console.log(event.target.value);
        setUsername(event.target.value);
    }

    function handlePasswordInput(event: any) {
        setPassword(event.target.value);
    }

    return (
        <div className="loginWrapper">
            <Form onSubmit={loginHandler}>
                <Form.Group className="mb-3" controlId="formGroupUsername">
                    <Form.Label>Username</Form.Label>
                    <Form.Control type="username" placeholder="Enter username" onChange={handleUsernameInput}/>
                </Form.Group>
                <Form.Group className="mb-3" controlId="formGroupPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Password" onChange={handlePasswordInput}/>
                </Form.Group>
                <Button type="submit" variant="primary">Login</Button>
            </Form>
            {passwordAlert}
        </div>
    )
}
