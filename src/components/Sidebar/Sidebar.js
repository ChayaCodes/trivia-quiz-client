import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

function Sidebar() {
    return (
        <div className="sidebar">
            <NavLink to="/" className="nav-button">בית</NavLink>
            <NavLink to="/quizzes" className="nav-button">חידונים</NavLink>
            <NavLink to="/create-quiz" className="nav-button">צור חידון</NavLink>
            <NavLink to="/login" className="nav-button">התחברות</NavLink>
            <NavLink to="/register" className="nav-button">הרשמה</NavLink>
        </div>
    );
}

export default Sidebar;