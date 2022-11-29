import React from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import {Nav} from "react-bootstrap";
import {LinkContainer} from 'react-router-bootstrap';

import "./styles.css"
import {Auth} from "../../models/Auth";

function HeaderNavbar() {
    const [isCheckingAdmin, setIsCheckingAdmin] = React.useState(true);
    const [isSignedIn, setIsSignedIn] = React.useState(false);

    React.useEffect(() => {
        getUserIfSignedIn();
        setIsCheckingAdmin(false);
    }, []);

    function getUserIfSignedIn() {
        const auth = Auth.getAuthFromLocalStorage();
        if (auth && auth.token.isValid()) {
            setIsSignedIn(true);
        }
    }

    function getUsernameOfSignedInUser() {
        const auth = Auth.getAuthFromLocalStorage();
        if (auth && auth.token.isValid()) {
            return auth.user.username;
        }
    }

    let loginComponent;
    if (!isCheckingAdmin) {
        if (isSignedIn) {
            loginComponent = <Navbar.Text>Signed in as: {getUsernameOfSignedInUser()}</Navbar.Text>
        } else {
            loginComponent = <LinkContainer to='/login'><Nav.Link>Login</Nav.Link></LinkContainer>
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
                            {loginComponent}
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </div>
    );
}

export default HeaderNavbar;