import {
    Navigate,
    useLocation,
} from "react-router-dom";


export function PrivateRoute({children}) {

    function isAuthenticated() {
        return localStorage.getItem('emwi-auto-moto-access-token') !== null;
    }
    let location = useLocation();

    if (!isAuthenticated()) {
        return <Navigate to="/login" state={{from: location}} replace/>;
    }

    return children;
}
