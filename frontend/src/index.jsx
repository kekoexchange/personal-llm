import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import 'mgplus/dist/css/mgplus.css';
import './index.css';

window.React = React;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);