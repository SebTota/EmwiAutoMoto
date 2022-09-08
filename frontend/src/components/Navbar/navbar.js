import React from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import {Nav} from "react-bootstrap";
import {LinkContainer} from 'react-router-bootstrap';

import "./styles.css"

function HeaderNavbar() {
    const [isCheckingAdmin, setIsCheckingAdmin] = React.useState(true);
    const [isAdmin, setIsAdmin] = React.useState(false);

    // componentDidMount()
    React.useEffect(() => {
        if (isSignedIn()) {
            setIsAdmin(true);
        }
        setIsCheckingAdmin(false);
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
            adminMessage = <Navbar.Text>Signed in as: {getUsernameOfSignedInUser()}</Navbar.Text>
        } else {
            adminMessage = <LinkContainer to='/login'><Navbar.Link>Login</Navbar.Link></LinkContainer>
        }
    }

    return (
        <div className="header">
            <Navbar collapseOnSelect expand="lg">
                <Container>
                    <LinkContainer to='/'><Navbar.Brand>EMWI Auto-Moto</Navbar.Brand></LinkContainer>
                    <Navbar.Toggle aria-controls="responsive-navbar-nav"/>
                    <Navbar.Collapse id="responsive-navbar-nav">
                        <Nav className="justify-content-start flex-grow-1 pe-3">
                            <LinkContainer to='/'><Nav.Link>Motorcycles</Nav.Link></LinkContainer>
                        </Nav>
                        <Nav className="justify-content-end flex-grow-1 pe-3">
                            <LinkContainer to='/contact'><Nav.Link>Contact</Nav.Link></LinkContainer>
                            {adminMessage}
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </div>
    );
}

export default HeaderNavbar;