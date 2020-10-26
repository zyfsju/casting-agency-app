import React from "react";
import logo from "../logo.svg";

const Hero = () => (
  <div className="text-center hero">
    <img className="mb-3 app-logo" src={logo} alt="React logo" width="120" />
    <h1 className="mb-4">React Casting</h1>
    <p className="lead">Let's discuss your casting needs over coffee!</p>
  </div>
);

export default Hero;
