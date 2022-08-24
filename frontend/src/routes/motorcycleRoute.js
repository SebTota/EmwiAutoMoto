import HeaderNavbar from "../components/Navbar/navbar";
import ItemPage from "../components/ItemPage";
import {useParams} from "react-router-dom";

export default function MotorcycleRoute() {
    let params = useParams();

    return (
        <div className="App">
            <HeaderNavbar/>
            <ItemPage id={params.id}/>
        </div>
    );
}