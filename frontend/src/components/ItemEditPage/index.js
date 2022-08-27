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

export default function ItemPage(props) {
    const [motorcycle, setMotorcycle] = React.useState(null);
    /**
     * Loading - Page Loading
     * Update - Updating an existing motorcycle
     * New - Adding a new motorcycle
     */
    const changeLoading = "Loading";
    const changeUpdate = "Update";
    const changeNew = "New";
    const [typeOfChange, setTypeOfChange] = React.useState(changeLoading); // TODO: Make this an Enum

    // componentDidMount()
    React.useEffect(() => {
        if (props.id !== 'new') {
            getMotorcycle(props.id).then(motorcycle => {
                setMotorcycle(motorcycle);
                setTypeOfChange(changeUpdate);
            })
        } else {
            setTypeOfChange(changeNew);
        }
    }, []);

    function getYear() {
        if (typeOfChange === changeUpdate) {
            return motorcycle.year;
        }
    }

    function getMake() {
        if (typeOfChange === changeUpdate) {
            return motorcycle.make;
        }
    }

    function getModel() {
        if (typeOfChange === changeUpdate) {
            return motorcycle.model;
        }
    }

    function getColor() {
        if (typeOfChange === changeUpdate) {
            return motorcycle.color;
        }
    }

    function getPrice() {
        if (typeOfChange === changeUpdate) {
            return motorcycle.price;
        }
    }

    function getOdometer() {
        if (typeOfChange === changeUpdate) {
            return motorcycle.odometer;
        }
    }

    function getOdometerMeasurement() {
        if (typeOfChange === changeUpdate) {
            return motorcycle.odometerMeasurement;
        }
    }

    function getStatus() {
        if (typeOfChange === changeUpdate) {
            return motorcycle.forSale;
        }
    }

    function saveChanges() {
        console.log('changes saved')
    }

    if (motorcycle === null && (typeOfChange === changeUpdate || typeOfChange === changeLoading)) {
        return (<h3>Loading...</h3>)
    } else {
        return (
            <div>
                <Form>
                    <Row className="mb-3">
                        <Form.Group as={Col} md={2} className="mb-3">
                            <Form.Label>Year</Form.Label>
                            <Form.Control type="number" placeholder="Year" defaultValue={getYear()}/>
                        </Form.Group>
                        <Form.Group as={Col} md={3} className="mb-3">
                            <Form.Label>Make</Form.Label>
                            <Form.Control placeholder="Make" defaultValue={getMake()}/>
                        </Form.Group>
                        <Form.Group as={Col} md={5} className="mb-3">
                            <Form.Label>Model</Form.Label>
                            <Form.Control placeholder="Model" defaultValue={getModel()}/>
                        </Form.Group>
                        <Form.Group as={Col} md={2} className="mb-3">
                            <Form.Label>Color</Form.Label>
                            <Form.Control placeholder="Color" defaultValue={getColor()}/>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group as={Col} md={3} className="mb-3">
                            <Form.Label>Price - Zloty/PLN</Form.Label>
                            <Form.Control type="number" placeholder="Price" defaultValue={getPrice()}/>
                        </Form.Group>
                        <Form.Group as={Col} md={7}>
                            <Row>
                                <Form.Group as={Col} md={6} className="mb-3">
                                    <Form.Label>Odometer</Form.Label>
                                    <Form.Control type="number" placeholder="Odometer" defaultValue={getOdometer()}/>
                                </Form.Group>
                                <Form.Group as={Col} md={6} className="mb-3">
                                    <Form.Label>Odometer Measurement</Form.Label>
                                    <Form.Select id="odometerMeasurementSelect" defaultValue={getOdometerMeasurement()}>
                                        <option>Miles</option>
                                        <option>Kilometers</option>
                                    </Form.Select>
                                </Form.Group>
                            </Row>
                        </Form.Group>
                        <Form.Group as={Col} md={2} className="mb-3">
                            <Form.Label>Status</Form.Label>
                            <Form.Select id="odometerMeasurementSelect" defaultValue={getStatus()}>
                                <option>For Sale</option>
                                <option>Sold</option>
                            </Form.Select>
                        </Form.Group>
                    </Row>
                    <Button variant="primary" onClick={() => {saveChanges()}}>Save</Button>
                </Form>
            </div>
        )
    }

}
