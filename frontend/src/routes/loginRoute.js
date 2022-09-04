import HeaderNavbar from "../components/Navbar/navbar";
import Login from "../components/Login";
import Container from "react-bootstrap/Container";

export default function LoginRoute() {
    return (
        <div className="App">
            <HeaderNavbar/>
            <Container>
                <Login/>
            </Container>
        </div>
    );
}