import React, {Component} from 'react';
import Container from 'react-bootstrap/Container';

import ListItem from "../ListItem";
import { getMotorcycles } from "../../controllers/StoreController";

import "./styles.css"


class ItemList extends Component {
    state = {
        motorcycles: null
    }

    componentDidMount() {
        getMotorcycles().then(motorcycles => {
            this._asyncRequest = null;
            this.setState({motorcycles})
        })
    }

    componentWillMount() {
        if (this._asyncRequest) {
            this._asyncRequest.cancel();
        }
    }

    render() {
        if (this.state.motorcycles === null) {
            return (<h3>Loading</h3>)
        } else {
            return (
                <Container className="items">
                    <div className="row">
                        {
                            this.state.motorcycles.map((motorcycle) => <div key={motorcycle.key} className="col-12 col-sm-6 col-md-4"><ListItem key={motorcycle.key} item={motorcycle}/></div>)
                        }
                    </div>
                </Container>
            );
        }
    }
}

export default ItemList;