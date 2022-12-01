import ItemEditPage from "../components/ItemEditPage";
import {useParams} from "react-router-dom";
import Container from "react-bootstrap/Container";

export default function EditMotorcycleRoute(props) {
    let params = useParams();

    return (
        <div className="App">
            <Container>
                <ItemEditPage id={params.id} type={props.type}/>
            </Container>
        </div>
    );
}