import React, { Component } from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { Link } from 'react-router';
import ListItem from "../ListItem";
import {Motorcycle} from "../../models/Motorcycle";
import "./styles.css"

const numMotorcyclesPerRow = 2;


function getMotorcycles() {
  const motorcycleOne = new Motorcycle('abc123', 2000, 'Kawasaki', 'Ninja', 1000, 'White',
      4000, 'Test description', false, [], [])
  const motorcycleTwo = new Motorcycle('a1', 2000, 'Suzuki', 'Something', 1000, 'White',
      4000, 'Test description', false, [], [])
  const motorcycleThree = new Motorcycle('b3', 2000, 'Honda', 'Motorcycle', 1000, 'White',
      4000, 'Test description', false, [], [])

  return [motorcycleOne, motorcycleTwo, motorcycleThree]
}

function mapMotorcyclesToRows(motorcycles) {
  const numRows = Math.ceil(motorcycles.length / numMotorcyclesPerRow);

  let res = [];
  for (let i = 0, j =0; i < numRows; i++, j+=numMotorcyclesPerRow) {
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
        <Row xs={1} md={2} className="g-4">
          { this.props.item.map((motorcycle =>
              <Col sm={12} lg={6} mt={3}><ListItem key={motorcycle.key} item={motorcycle} /></Col>)) }
          { emptyCols.map((emptyCol => <Col sm={12} lg={6} mb={3} key={emptyCol}></Col>)) }
        </Row>
    )
  }
}


class ItemPage extends Component {
  render() {
    const motorcycles = getMotorcycles();
    const rowMapping = mapMotorcyclesToRows(motorcycles);
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

export default ItemPage;