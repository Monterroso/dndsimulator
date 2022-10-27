import logo from './logo.svg';
import './App.css';
import {useEffect, useState} from "react"
import createGeneralObjectCreator from './constructors/generalObjectCreator';
import Display from './components/Display';

const filterOut = ["dict", "int", "float", "list", "str", "tuple", "NoneType"]

function App() {
  
  return (  
    <div className="App">
      <Display/>
    </div>
  );
}

export default App;
