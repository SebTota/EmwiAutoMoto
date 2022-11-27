import React, { Component } from 'react';
import { Link } from "react-router-dom";
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import "./styles.css"

class ListItem extends Component {
    render() {
        return(
            <Link to={`/motorcycle/${this.props.item.id}`} style={{ color: 'inherit', textDecoration: 'inherit'}}>
                <Card className="motorcycle-card-wrapper">
                    <Card.Img className="motorcycle-card-img" variant="top" src={this.props.item.thumbnail} />
                    <Card.Body className="shop-item-card">
                        <Row><Col className="shop-item-card-title-col"><span>{this.props.item.year + ' ' + this.props.item.make + ' ' + this.props.item.model}</span></Col></Row>
                        <Row>
                            <Col className="shop-item-card-price-col"><span>{this.props.item.price + "pln"}</span></Col>
                            <Col className="shop-item-card-km-col"><span>{this.props.item.km + "km"}</span></Col>
                        </Row>
                    </Card.Body>
                </Card>
            </Link>
        )
    }
}

export default ListItem;