import React from 'react';
import {useNavigate} from "react-router-dom";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import ImageGallery from 'react-image-gallery';
import {getMotorcycle} from "../../controllers/StoreController";

import "./styles.css"
import "react-image-gallery/styles/css/image-gallery.css";
import {Dropdown} from "react-bootstrap";

export default function ItemPage(props) {
    const navigate = useNavigate();
    const [motorcycle, setMotorcycle] = React.useState(null);
    const [apiCall, setApiCall] = React.useState(false);
    const [isAdmin, setIsAdmin] = React.useState(true);
    const [isEditing, setIsEditing] = React.useState(false);

    // componentDidMount()
    React.useEffect(() => {
        console.log(apiCall)
        if (apiCall === false) {
            setApiCall(true)
            getMotorcycle(props.id).then(motorcycle => {
                setMotorcycle(motorcycle)
            })
        }

    }, []);

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

    function getImages() {
        let images = motorcycle.images;
        images.map(image => {
            if (image.hasOwnProperty('image')) {
                image['original'] = image['image'];
                delete image['image'];
                return image;
            }
        })
        console.log(images)
        return images;
    }

    function enableEditing() {
        console.log('enabling editing')
        setIsEditing(true);
    }

    function saveChanges() {
        setIsEditing(false);
    }

    let adminButton;
    if (isAdmin) {
        if (!isEditing) {
            adminButton = <Button variant="warning" onClick={() => {
                enableEditing()
            }}>Edit</Button>;
        } else {
            adminButton = <Button variant="warning" onClick={() => {
                saveChanges()
            }}>Save</Button>;
        }
    }

    if (motorcycle === null) {
        return (<h3>Loading...</h3>)
    } else {
        return (
            <div>
                <Form>
                    <Row className="mb-3">
                        <Form.Group as={Col} md={2} className="mb-3">
                            <Form.Label>Year</Form.Label>
                            <Form.Control type="number" placeholder="Year"/>
                        </Form.Group>
                        <Form.Group as={Col} md={3} className="mb-3">
                            <Form.Label>Make</Form.Label>
                            <Form.Control placeholder="Make"/>
                        </Form.Group>
                        <Form.Group as={Col} md={5} className="mb-3">
                            <Form.Label>Model</Form.Label>
                            <Form.Control placeholder="Model"/>
                        </Form.Group>
                        <Form.Group as={Col} md={2} className="mb-3">
                            <Form.Label>Color</Form.Label>
                            <Form.Control placeholder="Color"/>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group as={Col} md={3} className="mb-3">
                            <Form.Label>Price - Zloty/PLN</Form.Label>
                            <Form.Control type="number" placeholder="Price"/>
                        </Form.Group>
                        <Form.Group as={Col} md={7}>
                            <Row>
                                <Form.Group as={Col} md={6} className="mb-3">
                                    <Form.Label>Odometer</Form.Label>
                                    <Form.Control type="number" placeholder="Odometer"/>
                                </Form.Group>
                                <Form.Group as={Col} md={6} className="mb-3">
                                    <Form.Label>Odometer Measurement</Form.Label>
                                    <Form.Select id="odometerMeasurementSelect">
                                        <option>Miles</option>
                                        <option>Kilometers</option>
                                    </Form.Select>
                                </Form.Group>
                            </Row>
                        </Form.Group>
                        <Form.Group as={Col} md={2} className="mb-3">
                            <Form.Label>Status</Form.Label>
                            <Form.Select id="odometerMeasurementSelect">
                                <option>For Sale</option>
                                <option>Sold</option>
                            </Form.Select>
                        </Form.Group>
                    </Row>
                </Form>
            </div>
        )
    }

}
