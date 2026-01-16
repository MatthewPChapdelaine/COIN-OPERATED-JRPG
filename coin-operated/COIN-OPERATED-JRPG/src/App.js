import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('COIN:OPERATED JRPG - Initializing...');

  useEffect(() => {
    setMessage('Welcome to COIN:OPERATED JRPG');
  }, []);

  return (
    <div className="app">
      <canvas id="game-canvas" width={1024} height={896}></canvas>
      <div className="ui">
        <h1>{message}</h1>
      </div>
    </div>
  );
}

export default App;
