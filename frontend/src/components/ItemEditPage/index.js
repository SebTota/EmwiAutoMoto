import React, {useEffect} from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import ImageGallery from 'react-image-gallery';
import {getMotorcycle, updateMotorcycle} from "../../controllers/storeController";

import "./styles.css"
import "react-image-gallery/styles/css/image-gallery.css";
import {ReactSortable} from "react-sortablejs";

export default function ItemEditPage(props) {
    // props - type ['edit' - editing an existing motorcycle, 'new' - creating a new motorcycle]
    // props - id [the id of the motorcycle that is being updated]

    const [motorcycle, setMotorcycle] = React.useState(null);
    const [images, setImages] = React.useState([]);

    /**
     * Loading - Page Loading
     * Update - Updating an existing motorcycle
     * New - Adding a new motorcycle
     */
    const changeLoading = "Loading";
    const changeUpdate = "Update";
    const changeNew = "New";
    const [typeOfChange, setTypeOfChange] = React.useState(changeLoading); // TODO: Make this an Enum

    const id = props.id;
    const type = props.type;

    // componentDidMount()
    React.useEffect(() => {
        if (type === 'edit') {
            getMotorcycle(id).then(motorcycle => {
                setMotorcycle(motorcycle);
                setTypeOfChange(changeUpdate);
                getImages(motorcycle);
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
            return motorcycle.odometer_measurement;
        }
    }

    function getIsSold() {
        if (typeOfChange === changeUpdate) {
            return motorcycle.sold;
        }
    }

    function getDescription() {
        if (typeOfChange === changeUpdate) {
            return motorcycle.description;
        }
    }

    function getImages(motorcycle) {
        let images = motorcycle.images;
        images.map(image => {
            if (image.hasOwnProperty('image')) {
                image['original'] = image['image'];
                delete image['image'];
                return image;
            }
        })
        setImages(images);
    }

    function getImageThumbnailList() {
        let imageThumbnailUrls = [];
        images.forEach((entry) => {
            imageThumbnailUrls.push(entry['thumbnail'])
        })
        return imageThumbnailUrls;
    }


    function saveChanges() {
        const year = document.getElementById('year').value;
        const make = document.getElementById('make').value;
        const model = document.getElementById('model').value;
        const color = document.getElementById('color').value;
        const price = document.getElementById('price').value;
        const odometer = document.getElementById('odometer').value;
        const odometerMeasurement = document.getElementById('odometerMeasurementSelect').value;
        const isSold = document.getElementById('isSold').value;
        const description = document.getElementById('description').value;

        const changes = {
            'year': year,
            'make': make,
            'model': model,
            'color': color,
            'price': price,
            'odometer': odometer,
            'odometer_measurement': odometerMeasurement,
            'sold': isSold,
            'description': description
        }

        console.log(`Updating ${id} with changes: `, changes);

        updateMotorcycle(id, changes).then((data) => {
            console.log(`Response from update motorcycle request: ${data}`);
        })
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
                            <Form.Control id="year" type="number" placeholder="Year" defaultValue={getYear()}/>
                        </Form.Group>
                        <Form.Group as={Col} md={3} className="mb-3">
                            <Form.Label>Make</Form.Label>
                            <Form.Control id="make" placeholder="Make" defaultValue={getMake()}/>
                        </Form.Group>
                        <Form.Group as={Col} md={5} className="mb-3">
                            <Form.Label>Model</Form.Label>
                            <Form.Control id="model" placeholder="Model" defaultValue={getModel()}/>
                        </Form.Group>
                        <Form.Group as={Col} md={2} className="mb-3">
                            <Form.Label>Color</Form.Label>
                            <Form.Control id="color" placeholder="Color" defaultValue={getColor()}/>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group as={Col} md={3} className="mb-3">
                            <Form.Label>Price - Zloty/PLN</Form.Label>
                            <Form.Control id="price" type="number" placeholder="Price" defaultValue={getPrice()}/>
                        </Form.Group>
                        <Form.Group as={Col} md={7}>
                            <Row>
                                <Form.Group as={Col} md={6} className="mb-3">
                                    <Form.Label>Odometer</Form.Label>
                                    <Form.Control id="odometer" type="number" placeholder="Odometer"
                                                  defaultValue={getOdometer()}/>
                                </Form.Group>
                                <Form.Group as={Col} md={6} className="mb-3">
                                    <Form.Label>Odometer Measurement</Form.Label>
                                    <Form.Select id="odometerMeasurementSelect" defaultValue={getOdometerMeasurement()}>
                                        <option value="mi">Miles</option>
                                        <option value="km">Kilometers</option>
                                    </Form.Select>
                                </Form.Group>
                            </Row>
                        </Form.Group>
                        <Form.Group as={Col} md={2} className="mb-3">
                            <Form.Label>Status</Form.Label>
                            <Form.Select id="isSold" defaultValue={getIsSold()}>
                                <option value="false">For Sale</option>
                                <option value="true">Sold</option>
                            </Form.Select>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group className="mb-3">
                            <Form.Label>Description</Form.Label>
                            <Form.Control
                                id="description"
                                defaultValue={getDescription()}
                                as="textarea"
                                placeholder="Description"
                                style={{height: '120px'}}
                            />
                        </Form.Group>
                    </Row>
                    <Row>
                        <div className="image-gallery-wrapper">
                            <ImageGallery className="image-gallery-obj" items={images}/>
                        </div>
                    </Row>
                    <Row>
                        <div className="sortable-list-wrapper">
                            <ReactSortable list={images} setList={setImages} className="row">
                                {
                                    getImageThumbnailList().map((photoUrl) =>
                                        <div className="col-xs-4 col-sm-4 col-md-3 col-lg-2 sortable-wrapper">
                                            <div className="sortable-image-wrapper">
                                                <img className="sortable-image" src={photoUrl}/>
                                            </div>
                                            <div>
                                                <Button variant="danger" className="sortable-remove-button">Delete</Button>
                                            </div>
                                        </div>)
                                }
                            </ReactSortable>
                        </div>
                    </Row>
                    <Button variant="primary" className="m-5" onClick={() => {
                        saveChanges()
                    }}>Save</Button>
                </Form>
            </div>
        )
    }

}
