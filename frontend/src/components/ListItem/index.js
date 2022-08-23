import React, { Component } from 'react';
import { Link } from "react-router-dom";
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import "./styles.css"

class ListItem extends Component {
    render() {
        return(
            <Card>
                <Card.Img variant="top" src="https://2yrh403fk8vd1hz9ro2n46dd-wpengine.netdna-ssl.com/wp-content/uploads/2020/03/2020-kawasaki-ninja-650-buyers-guide-specs-prices-4.jpg" />
                <Card.Title>
                    <Row>
                        <Col>
                            {this.props.item.year + ' ' + this.props.item.make + ' ' + this.props.item.model}
                        </Col>
                        <Col>
                            {this.props.item.price + "zł"}
                        </Col>
                    </Row>
                </Card.Title>
                <Card.Body>
                    <p>Test</p>
                </Card.Body>
            </Card>
        )
    }
}

export default ListItem;