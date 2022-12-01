import {
    Navigate, Route,
    useLocation,
} from "react-router-dom";
import {UserState} from "../models/UserState";
import {Redirect} from "react-router";


function Component() {
    return null;
}

export function PrivateRoute({ element: ReactElement, ...rest }) {

    const [isLoading, setIsLoading] = React.useState(true);
    const [isAdmin, setIsAdmin] = React.useState(false);

    let location = useLocation();

    return (
        <Route
          {...rest}
          render={props =>
            !isLoaded ? (
              <></>
            ) : user ? (
              < {...props} />
            ) : (
              <Redirect to='/login' />
            )
          }
        />
      );


    if (!isLoading) {
        if (!isAdmin) {
            return <Navigate to="/login" state={{from: location}} replace/>;
        } else {
            return Route
        }
    }



    <Route element={}

    return children;
}
