import React from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import {Nav} from "react-bootstrap";

import "./styles.css"

function HeaderNavbar() {
    const [isCheckingAdmin, setIsCheckingAdmin] = React.useState(true);
    const [isAdmin, setIsAdmin] = React.useState(false);

    // componentDidMount()
    React.useEffect(() => {
        if (isSignedIn()) {
            setIsAdmin(true);
            setIsCheckingAdmin(false);
        }
    }, []);

    function isSignedIn() {
        return localStorage.getItem('emwi-auto-moto-username') !== null;
    }

    function getUsernameOfSignedInUser() {
        return localStorage.getItem('emwi-auto-moto-username');
    }

    let adminMessage;
    if (!isCheckingAdmin) {
        if (isAdmin) {
        adminMessage = <Navbar.Text>Signed in as: <a>{getUsernameOfSignedInUser()}</a></Navbar.Text>
        } else {
            adminMessage = <Nav.Link href="/login">Login</Nav.Link>
        }
    }

    return (
        <div className="header">
            <Navbar collapseOnSelect expand="lg">
                <Container>
                    <Navbar.Brand href="/"><h1>EMWI Auto-Moto</h1></Navbar.Brand>
                    <Navbar.Toggle aria-controls="responsive-navbar-nav"/>
                    <Navbar.Collapse id="responsive-navbar-nav">
                        <Nav className="justify-content-end flex-grow-1 pe-3">
                            {adminMessage}
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </div>
    );
}

export default HeaderNavbar;