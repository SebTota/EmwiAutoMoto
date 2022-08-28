import HeaderNavbar from "../components/Navbar/navbar";
import ItemEditPage from "../components/ItemEditPage";
import {useParams} from "react-router-dom";

export default function EditMotorcycleRoute(props) {
    let params = useParams();

    return (
        <div className="App">
            <HeaderNavbar/>
            <ItemEditPage id={params.id} type={props.type}/>
        </div>
    );
}