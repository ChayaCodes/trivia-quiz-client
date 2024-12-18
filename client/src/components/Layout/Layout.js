import React from "react";
import Sidebar from "../Sidebar/Sidebar";
import "./Container.css";

function Container({ children }) {
  return (
    <>
      <div className="container">
        <Sidebar />
        <div className="content">{children}</div>
      </div>
      <footer className="footer">
        <span>
          פותח באהבה ❤️ על ידי חיה קרמר | צור קשר: chaya41182@gmail.com |
          טלפון: 058-3241182
        </span>
      </footer>
    </>
  );
}

export default Container;
