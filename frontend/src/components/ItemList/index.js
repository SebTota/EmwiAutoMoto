import React, {Component} from 'react';
import Container from 'react-bootstrap/Container';

import ListItem from "../ListItem";
import {getMotorcycles} from "../../controllers/storeController";

import "./styles.css"
import {isAdmin} from "../../utils/utils";
import Button from "react-bootstrap/Button";

export default function ItemList(props) {
    const [motorcycleResponse, setMotorcycleResponse] = React.useState(null);

    const selectedForSaleOptionClass = 'product-grid-header-show-active';
    const showForSaleButton = React.createRef();
    const showSoldButton = React.createRef();
    const showInactiveButton = React.createRef();

    // componentDidMount()
    React.useEffect(() => {
        getMotorcyclesOnLoad();
        setButtonsOnLoad();
    }, []);

    function getMotorcyclesOnLoad() {
        const urlParams = new URLSearchParams(window.location.search);
        const showSold = urlParams.has('showSold') ? urlParams.get('showSold') : 'false';
        const showStatus = urlParams.has('showStatus') ? urlParams.get('showStatus') : 'active';
        const page = urlParams.has('page') ? urlParams.get('page') : '1';

        getMotorcycles(showSold, showStatus, page).then(motorcycles => {
            setMotorcycleResponse(motorcycles);
        })
    }

    function setButtonsOnLoad() {
        const urlParams = new URLSearchParams(window.location.search);
        const showSold = urlParams.has('showSold') ? urlParams.get('showSold') : 'false';
        const showStatus = urlParams.has('showStatus') ? urlParams.get('showStatus') : 'active';

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
        getMotorcycles(showSold, showStatus, page).then(motorcycles => {
            setMotorcycleResponse(motorcycles);
        });
    }

    function showMotorcyclesHandler(showSold) {
        if (showSold) {
            showForSaleButton.current.classList.remove(selectedForSaleOptionClass);
            showSoldButton.current.classList.add(selectedForSaleOptionClass);
        } else {
            showSoldButton.current.classList.remove(selectedForSaleOptionClass);
            showForSaleButton.current.classList.add(selectedForSaleOptionClass);
        }
        onMotorcycleSearchChange();
    }

    function toggleShowInactiveMotorcycles() {
        if (showInactiveButton.current.classList.contains(selectedForSaleOptionClass)) {
            showInactiveButton.current.classList.remove(selectedForSaleOptionClass);
        } else {
            showInactiveButton.current.classList.add(selectedForSaleOptionClass);
        }
        onMotorcycleSearchChange();
    }

    function showBackPageButton() {
        return motorcycleResponse && motorcycleResponse.page > 1;
    }

    function showNextPageButton() {
        return motorcycleResponse && motorcycleResponse.has_next_page;
    }

    function goToNextPage() {
        setMotorcycleResponse(null);
        getMotorcycles(false, 'active', motorcycleResponse.page + 1).then(motorcycles => {
            setMotorcycleResponse(motorcycles);
        })
    }

    function goToPreviousPage() {
        getMotorcycles(false, 'active', motorcycleResponse.page - 1).then(motorcycles => {
            setMotorcycleResponse(motorcycles);
        })
    }

    function addNewMotorcycle() {
        window.location.href = '/motorcycle/new'
    }

    let listBody = (<h3>Loading</h3>);
    if (motorcycleResponse !== null) {
        listBody = (<div className="row">
            {
                motorcycleResponse.items.map((motorcycle) => <div key={motorcycle.id} className="col-sm-6 col-md-6 col-lg-4">
                    <ListItem item={motorcycle}/></div>)
            }
        </div>)
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

