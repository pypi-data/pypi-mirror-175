import "./App.css";
import { useEffect } from 'react';
import axios from 'axios';

function App() {
  const backend_url = 'http://localhost:5000'
  let data = "";

  useEffect(() => {
    setTimeout(() => {
      axios.get(backend_url)
      .then(res => {
        console.log(res)
        data = res.data;
      })
    }, 1000);
  }, []);


  return (
    <div className="app">
      <h1>{ data }</h1>
      <h4>Data from Backend at { backend_url }</h4>
    </div>
  );
}

export default App;
