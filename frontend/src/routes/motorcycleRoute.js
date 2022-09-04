import HeaderNavbar from "../components/Navbar/navbar";
import ItemPage from "../components/ItemPage";
import {useParams} from "react-router-dom";
import Container from "react-bootstrap/Container";

export default function MotorcycleRoute() {
    let params = useParams();

    return (
        <div className="App">
            <HeaderNavbar/>
            <Container>
                <ItemPage id={params.id}/>
            </Container>
        </div>
    );
}