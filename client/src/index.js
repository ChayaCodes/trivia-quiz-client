// import {StrictMode} from 'react';
import {createRoot} from 'react-dom/client';
import App from './App';
import React from "react";





const rootElement = document.getElementById('root');
const root = createRoot(rootElement);

root.render(
  // <StrictMode>
    <App />
  // </StrictMode>,
);

// // ReactDOM.render(
// //   <React.StrictMode>
// //     <App />
// //   </React.StrictMode>,
// //   document.getElementById('root')
// // );
