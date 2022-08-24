import React, {Component} from 'react';
import {Link} from "react-router-dom";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import "./styles.css"
import {getMotorcycle} from "../../controllers/StoreController";

class ItemPage extends Component {
    state = {
        motorcycle: null
    };

    componentDidMount() {
        getMotorcycle(this.props.id).then(motorcycle => {
            this._asyncRequest = null;
            console.log(motorcycle)
            this.setState({motorcycle})
        })
    }

    componentWillMount() {
        if (this._asyncRequest) {
            this._asyncRequest.cancel();
        }
    }

    getTitle = () => {
        return `${this.state.motorcycle.year} ${this.state.motorcycle.make} ${this.state.motorcycle.model}`;
    }

    getPrice = () => {
        return `${this.state.motorcycle.price} zł`;
    }

    render() {
        if (this.state.motorcycle === null) {
            return (<h3>Loading...</h3>)
        }

        return (
            <Row xs={1} sm={1} md={2}>
                <Col>

                </Col>
                <Col>
                    <div className="textAlignLeft">
                        <div className="small mb-3">
                            <Link className="backToHomeLink" to="/" style={{ textDecoration: 'inherit'}}>
                            <span>
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                   className="bi bi-arrow-left-short" viewBox="0 0 16 16">
                                  <path fill-rule="evenodd"
                                        d="M12 8a.5.5 0 0 1-.5.5H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H11.5a.5.5 0 0 1 .5.5z"/>
                                </svg>
                            </span> Wszystkie Motocykle
                            </Link>
                        </div>

                        <h3 className="itemName">{this.getTitle()}</h3>
                        <p className="itemCost frm">{this.getPrice()}</p>
                        <p className="description">
                            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ea nulla modi, odit explicabo hic
                            doloremque commodi ab molestiae. Iure voluptatem labore et aliquid soluta inventore expedita
                            quam vel a earum!
                        </p>
                        <button className="normalBtn">Kontakt</button>
                    </div>
                </Col>
            </Row>
        )
    }
}

export default ItemPage;