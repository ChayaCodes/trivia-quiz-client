import React from 'react';
import './FrontCard.css';

const FrontCard = ({ image, name }) => {
  return (
    <>
      <img src={image} alt={name} />
      <h3>{name}</h3>
    </>
  );
};

export default FrontCard;