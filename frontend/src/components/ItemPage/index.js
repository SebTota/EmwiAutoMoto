import React from 'react';
import {useNavigate} from "react-router-dom";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import ImageGallery from 'react-image-gallery';
import {getMotorcycle} from "../../controllers/StoreController";

import "./styles.css"
import "react-image-gallery/styles/css/image-gallery.css";

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

    function goBack() {
        if (!isEditing) {
            navigate(-1);
        }
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
            adminButton = <Button variant="warning" onClick={() => {enableEditing()}}>Edit</Button>;
        } else {
            adminButton = <Button variant="warning" onClick={() => {saveChanges()}}>Save</Button>;
        }
    }

    if (motorcycle === null) {
        return (<h3>Loading...</h3>)
    } else {
        return (
            <div>
                <Row className="detailedViewRowWrapper">
                    <Col lg={8}>
                        <div className="image-gallery-wrapper">
                            <ImageGallery className="image-gallery-obj" items={getImages()} />
                        </div>
                    </Col>
                    <Col lg={4}>
                        <div className="textAlignLeft">
                            <div className="small mb-3">
                                <div className="backToHomeLink" onClick={() => {goBack()}}>
                                <span>
                                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                       className="bi bi-arrow-left-short" viewBox="0 0 16 16">
                                      <path fillRule="evenodd"
                                            d="M12 8a.5.5 0 0 1-.5.5H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H11.5a.5.5 0 0 1 .5.5z"/>
                                    </svg>
                                </span> Wszystkie Motocykle
                                </div>
                            </div>

                            <h3 className="itemName" contentEditable={isEditing} >{getTitle()}</h3>
                            <Row>
                                <Col>
                                    <h5 className="itemCost" contentEditable={isEditing}>{getPrice()}</h5>
                                </Col>
                                <Col className="textAlignRight">
                                    <p className="itemCost" contentEditable={isEditing}>{getOdometerReading()}</p>
                                </Col>
                            </Row>
                            <p className="description" contentEditable={isEditing}>{getListingDescription()}</p>
                        </div>
                        {adminButton}
                    </Col>
                </Row>
            </div>
        )
    }

}
