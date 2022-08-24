import React, {Component} from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import ListItem from "../ListItem";
import { getMotorcycles } from "../../controllers/StoreController";

import "./styles.css"

const numMotorcyclesPerRowExtraSmall = 1;
const numMotorcyclesPerRowMedium = 2;
const numMotorcyclesPerRow = 3;

function mapMotorcyclesToRows(motorcycles) {
    const numRows = Math.ceil(motorcycles.length / numMotorcyclesPerRow);

    let res = [];
    for (let i = 0, j = 0; i < numRows; i++, j += numMotorcyclesPerRow) {
        res[i] = [];
        res[i] = motorcycles.slice(j, j + numMotorcyclesPerRow);
    }

    return res;
}


class ItemRow extends Component {
    render() {
        const addNumEmptyCols = numMotorcyclesPerRow - this.props.item.length;
        const emptyCols = [];

        for (let i = 0; i < addNumEmptyCols; i++) {
            emptyCols.push(i);
        }

        return (
            <Row xs={numMotorcyclesPerRowExtraSmall} md={numMotorcyclesPerRowMedium} lg={numMotorcyclesPerRow} className="g-4">
                {this.props.item.map((motorcycle =>
                    <Col><ListItem key={motorcycle.key} item={motorcycle}/></Col>))}
                {emptyCols.map((emptyCol => <Col key={emptyCol}></Col>))}
            </Row>
        )
    }
}


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
            const rowMapping = mapMotorcyclesToRows(this.state.motorcycles);
            let rowNum = 0;

            return (
                <Container className="items">
                    {
                        rowMapping.map((row) => <ItemRow key={rowNum++} item={row}></ItemRow>)
                    }
                </Container>
            );
        }
    }
}

export default ItemList;