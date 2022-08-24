import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import {Nav} from "react-bootstrap";

import "./styles.css"

function HeaderNavbar() {
  return (
      <div className="header">
        <Navbar collapseOnSelect expand="lg">
        <Container>
          <Navbar.Brand href="/"><h1>EMWI Auto-Moto</h1></Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="justify-content-end flex-grow-1 pe-3" >
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      </div>
  );
}

export default HeaderNavbar;