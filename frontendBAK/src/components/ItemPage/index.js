import React from 'react';
import {Link} from "react-router-dom";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import ImageGallery from 'react-image-gallery';
import {deleteMotorcycle, getMotorcycle} from "../../controllers/storeController";

import "./styles.css"
import "react-image-gallery/styles/css/image-gallery.css";
import {Alert} from "react-bootstrap";

export default function ItemPage(props) {
    const [motorcycle, setMotorcycle] = React.useState(null);
    const [isAdmin, setIsAdmin] = React.useState(false);
    const [showRemoveAlert, setShowRemoveAlert] = React.useState(false);

    const id = props.id;

    // componentDidMount()
    React.useEffect(() => {
        isAdmin().then(r => {
            setIsAdmin(r);
        })
        getMotorcycle(id).then(motorcycle => {
            setMotorcycle(motorcycle)
        })
    }, []);

    function goBack() {
        window.location.href = '/';
    }

    function getTitle() {
        return `${motorcycle.year} ${motorcycle.make} ${motorcycle.model}`;
    }

    function getPrice() {
        return `${motorcycle.price} pln`;
    }

    function getOdometerReading() {
        return `${motorcycle.km} km`
    }

    function getListingDescription() {
        return motorcycle.description
    }

    function deleteMotorcycleHandler() {
        setShowRemoveAlert(false);
        console.log(`Deleting motorcycle: ${id}`);
        deleteMotorcycle(id).then(r => {
            console.log(`Response form deleting motorcycle request: ${r}`);
            window.location.href = '/';
        }).catch(err => {
            console.log(`Failed to delete motorcycle.`, err);
        })
    }

    function getImages() {
        let images = motorcycle.images;
        if (!images) {
            return [];
        }

        images.map(image => {
            if (image.hasOwnProperty('image_url')) {
                image['original'] = image['image_url'];
                delete image['image_url'];
                return image;
            }
            return image;
        })
        return images;
    }

    let editButton;
    if (isAdmin()) {
        editButton = (
            <div>
                <Link to={`/motorcycle/edit/${id}`}>
                    <Button variant="warning" className="m-1">Edit</Button>
                </Link>
                <Button variant="danger" className="m-1" onClick={() => setShowRemoveAlert(true)}>Remove</Button>
                <Alert className="m-3" show={showRemoveAlert} variant="danger"
                       onClose={() => setShowRemoveAlert(false)}>
                    <Alert.Heading>Are you use you want to delete this motorcycle?</Alert.Heading>
                    <p>
                        This action can not be undone. Are you sure you want to delete this motorcycle?
                    </p>
                    <hr/>
                    <div className="d-flex justify-content-evenly">
                        <Button onClick={() => setShowRemoveAlert(false)} variant="outline-success">
                            Close
                        </Button>
                        <Button onClick={() => deleteMotorcycleHandler()} variant="outline-danger">
                            DELETE
                        </Button>
                    </div>
                </Alert>
            </div>
        )
    }

    if (motorcycle === null) {
        return (<h3>Loading...</h3>)
    } else {
        return (
            <div>
                <Row className="detailedViewRowWrapper">
                    <Col lg={8}>
                        <div className="image-gallery-wrapper">
                            <ImageGallery className="image-gallery-obj" items={getImages()}/>
                        </div>
                    </Col>
                    <Col lg={4}>
                        <div className="textAlignLeft">
                            <div className="small mb-3">
                                <Link className="backToHomeLink" to={'/'}>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                       className="bi bi-arrow-left-short" viewBox="0 0 16 16">
                                      <path fillRule="evenodd"
                                            d="M12 8a.5.5 0 0 1-.5.5H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H11.5a.5.5 0 0 1 .5.5z"/>
                                    </svg>
                                    Wszystkie Motocykle
                                </Link>
                            </div>

                            <h3 className="itemName">{getTitle()}</h3>
                            <Row>
                                <Col>
                                    <h5 className="itemCost">{getPrice()}</h5>
                                </Col>
                                <Col className="textAlignRight">
                                    <p className="itemCost">{getOdometerReading()}</p>
                                </Col>
                            </Row>
                            <p className="description">{getListingDescription()}</p>
                        </div>
                        {editButton}
                    </Col>
                </Row>
            </div>
        )
    }
}
