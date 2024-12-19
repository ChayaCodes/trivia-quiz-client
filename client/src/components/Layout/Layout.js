import React from 'react';
import "./Layout.css";
import Sidebar from '../Sidebar/Sidebar';
import Footer from '../Footer/Footer'; 

function Layout({ children }) {
  return (
    <div className="layout">
      <div className="container">
        <Sidebar />
        <div className="content">{children}</div>
      </div>
      <Footer /> 
    </div>
  );
}

export default Layout;