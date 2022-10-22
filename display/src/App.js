import logo from './logo.svg';
import './App.css';
import {useEffect, useState} from "react"

const filterOut = ["dict", "int", "float", "list", "str", "tuple", "NoneType"]

function App() {
  const [data, setData] = useState()
  useEffect(() => {
    fetch("data/text.json")
    .then( response => response.json())
    .then( data => setData(data))
  }, [])
  console.log(data)
  
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <div>
        {
          data != null && data.map(dataList => {
            const dataObj = {}

            dataList.forEach(info => {
              let {type} = info
              {/* if (filterOut.includes(type)) {
                type = "other"
              } */}
              if (dataObj[type] == null) {
                dataObj[type] = 0
              }

              dataObj[type] += 1
              {/* if (type === "Board") {
                Object.keys(info).forEach( key => {
                  dataObj[key] = 
                })
              } */}

              
            })
            return JSON.stringify(dataObj)
          })
        }
      </div>
    </div>
  );
}

export default App;
