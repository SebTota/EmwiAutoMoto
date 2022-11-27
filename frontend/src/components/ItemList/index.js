import React, {Component} from 'react';
import Container from 'react-bootstrap/Container';

import ListItem from "../ListItem";
import {getMotorcycles} from "../../controllers/storeController";

import "./styles.css"
import {isAdmin} from "../../utils/utils";
import Button from "react-bootstrap/Button";
import {
  useNavigate,
  createSearchParams,
} from 'react-router-dom';

export default function ItemList(props) {
    const navigate = useNavigate();

    const defaultParams = Object.freeze({'page': 1, 'show_sold': false, 'show_status': 'active'});
    const params = {'page': 1, 'show_sold': false, 'show_status': 'active'};

    const [waitingForApiResponse, setWaitingForApiResponse] = React.useState(true);
    const [motorcycleResponse, setMotorcycleResponse] = React.useState(null);

    const selectedForSaleOptionClass = 'product-grid-header-show-active';
    const showForSaleButton = React.createRef();
    const showSoldButton = React.createRef();
    const showInactiveButton = React.createRef();

    // componentDidMount()
    React.useEffect(() => {
        getQueryParamsOnLoad();
        updateMotorcycleList();
        setButtonsOnLoad();
    }, []);

    function getQueryParamsOnLoad() {
        const urlParams = new URLSearchParams(window.location.search);

        params['show_sold'] = urlParams.has('show_sold') ? urlParams.get('show_sold') : false;
        params['show_status'] = urlParams.has('show_status') ? urlParams.get('show_status') : 'active';
        params['page'] = urlParams.has('page') ? urlParams.get('page') : 1;
    }

    function updateMotorcycleList() {
        /**
         * Update the motorcycle list and query params to represent the motorcycles being shown
         */

        /**
         * Create a dictionary of ONLY the query params that are not default
         * Ex: if we are only showing for sale motorcycles, we don't need that in the query params
         * since that is default behavior
         */
        let p = {};
        for (const param in params) {
            if (defaultParams[param] !== params[param]) {
                console.log(defaultParams[param], params[param])
                p[param] = params[param];
            }
        }

        navigate({
            pathname: '',
            search: `?${createSearchParams(p)}`
        })

        setWaitingForApiResponse(true);
        getMotorcycles(params['show_sold'], params['show_status'], params['page']).then(motorcycles => {
            console.log(motorcycles)
            setMotorcycleResponse(motorcycles);
            setWaitingForApiResponse(false);
        })
    }

    function setButtonsOnLoad() {
        const urlParams = new URLSearchParams(window.location.search);
        const showSold = urlParams.has('show_sold') ? urlParams.get('show_sold') : 'false';
        const showStatus = urlParams.has('show_status') ? urlParams.get('show_status') : 'active';

        if (showSold === 'true') {
            showSoldButton.current.classList.add('product-grid-header-show-active')
        } else {
            showForSaleButton.current.classList.add('product-grid-header-show-active')
        }

        if (showStatus === 'inactive') {
            showInactiveButton.current.classList.add(selectedForSaleOptionClass);
        }
    }

    function onMotorcycleSearchChange(page=motorcycleResponse.page) {
        setMotorcycleResponse(null);
        const showSold = showSoldButton.current.classList.contains(selectedForSaleOptionClass);

        let showStatus;
        if (showInactiveButton.current === null || !showInactiveButton.current.classList.contains(selectedForSaleOptionClass)) {
            showStatus = 'active';
        } else {
            showStatus = 'inactive';
        }

        params['show_status'] = showStatus;
        params['show_sold'] = showSold;
        params['page'] = page;
        updateMotorcycleList();
    }

    function showMotorcyclesHandler(showSold) {
        if (showSold) {
            showForSaleButton.current.classList.remove(selectedForSaleOptionClass);
            showSoldButton.current.classList.add(selectedForSaleOptionClass);
        } else {
            showSoldButton.current.classList.remove(selectedForSaleOptionClass);
            showForSaleButton.current.classList.add(selectedForSaleOptionClass);
        }
        onMotorcycleSearchChange(1);
    }

    function toggleShowInactiveMotorcycles() {
        if (showInactiveButton.current.classList.contains(selectedForSaleOptionClass)) {
            showInactiveButton.current.classList.remove(selectedForSaleOptionClass);
        } else {
            showInactiveButton.current.classList.add(selectedForSaleOptionClass);
        }
        onMotorcycleSearchChange(1);
    }

    function showBackPageButton() {
        return motorcycleResponse && motorcycleResponse.page > 1;
    }

    function showNextPageButton() {
        return motorcycleResponse && motorcycleResponse.has_next_page;
    }

    function goToNextPage() {
        onMotorcycleSearchChange(motorcycleResponse.page + 1);
    }

    function goToPreviousPage() {
        onMotorcycleSearchChange(motorcycleResponse.page - 1);
    }

    function addNewMotorcycle() {
        navigate({
            pathname: '/motorcycle/new',
        })
    }

    let listBody = (<h3>Loading</h3>);
    if (!waitingForApiResponse) {
        if (motorcycleResponse && motorcycleResponse.motorcycles) {
            if (motorcycleResponse.motorcycles.length > 0) {
                listBody = (<div className="row">
                                {
                                    motorcycleResponse.motorcycles.map((motorcycle) => <div key={motorcycle.id} className="col-sm-6 col-md-6 col-lg-4">
                                        <ListItem item={motorcycle}/></div>)
                                }
                            </div>)
            } else {
                listBody = (<div className="alert alert-warning" role="alert">
                            Looks like there are no motorcycles with those search filters available right now!
                            </div>)
            }
        } else {
            listBody = (
                <div className="alert alert-danger" role="alert">
                Uh oh! An error occurred. Please try again later.
                </div>
            )
        }
    }

    let adminActions = <div></div>
    if (isAdmin()) {
        adminActions = (<div>
                            <span>Actions: </span>
                            <a className="product-grid-header-add-new-btn" onClick={addNewMotorcycle}>Add New Motorcycle</a>
                        </div>)
    }

    let adminShowProductOptions;
    if (isAdmin()) {
        adminShowProductOptions = (<a ref={showInactiveButton}
                       onClick={toggleShowInactiveMotorcycles} className="product-grid-header-show me-2">Inactive</a>)
    }

    return (
        <Container>
            <header className="product-grid-header">
                {adminActions}
                <div>
                    <span className="me-2">Show: </span>
                    <a ref={showForSaleButton}
                       onClick={() => {
                           showMotorcyclesHandler(false)
                       }}
                       className="product-grid-header-show me-2">For Sale</a>
                    <a ref={showSoldButton}
                       onClick={() => {
                           showMotorcyclesHandler(true)
                       }} className="product-grid-header-show me-2">Sold</a>
                    {adminShowProductOptions}
                </div>
            </header>
            {listBody}
            <div>
                {showBackPageButton() ? <Button variant="outline-secondary" className="m-1 me-2" onClick={goToPreviousPage}>Prev</Button> : null}
                {showNextPageButton() ? <Button variant="outline-secondary" className="m-1 ms-2" onClick={goToNextPage}>Next</Button> : null}
            </div>
        </Container>
    );
}

