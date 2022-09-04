import React, {Component} from 'react';
import Container from 'react-bootstrap/Container';

import ListItem from "../ListItem";
import {getMotorcycles} from "../../controllers/storeController";

import "./styles.css"
import {isAdmin} from "../../utils/utils";

export default function ItemList(props) {
    const [motorcycles, setMotorcycles] = React.useState(null);

    const selectedForSaleOptionClass = 'product-grid-header-show-active';
    const showForSaleButton = React.createRef();
    const showSoldButton = React.createRef();

    // componentDidMount()
    React.useEffect(() => {
        getMotorcycles().then(motorcycles => {
            setMotorcycles(motorcycles)
        })
    }, []);

    function showMotorcyclesHandler(showSold) {
        if (showSold && showSoldButton.current.classList.contains(selectedForSaleOptionClass)) {
            return;
        }

        if (!showSold && showForSaleButton.current.classList.contains(selectedForSaleOptionClass)) {
            return;
        }

        setMotorcycles(null);
        if (showSold) {
            showForSaleButton.current.classList.remove(selectedForSaleOptionClass);
            showSoldButton.current.classList.add(selectedForSaleOptionClass);
        } else {
            showSoldButton.current.classList.remove(selectedForSaleOptionClass);
            showForSaleButton.current.classList.add(selectedForSaleOptionClass);
        }
        getMotorcycles(showSold).then(motorcycles => {
            setMotorcycles(motorcycles);
        })
    }

    function addNewMotorcycle() {
        window.location.href = '/motorcycle/new'
    }

    let listBody = (<h3>Loading</h3>);
    if (motorcycles !== null) {
        listBody = (<div className="row">
            {
                motorcycles.map((motorcycle) => <div key={motorcycle.id} className="col-sm-6 col-md-6 col-lg-4">
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
                       className="product-grid-header-show product-grid-header-show-active me-2">For Sale</a>
                    <a ref={showSoldButton}
                       onClick={() => {
                           showMotorcyclesHandler(true)
                       }} className="product-grid-header-show me-2">Sold</a>
                </div>
            </header>
            {listBody}
        </Container>
    );
}

