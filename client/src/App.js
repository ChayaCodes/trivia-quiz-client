import "./App.css";
import React from "react";
import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Home from "./pages/HomePage/HomePage";
import Login from "./pages/LoginForm/LoginForm";
import Register from "./pages/RegisterForm/RegisterForm";
import CreateQuiz from "./pages/CreateQuiz/CreateQuiz";
import QuizPage from "./pages/QuizPage/QuizPage";
import Quizzes from "./pages/Quizzes/Quizzes";
import Layout from "./components/Layout/Layout"
import ProtectedRoute from "./components/ProtectedRoute";
function App() {
  const [userName, setUserName] = useState(null);
  const isLoggedIn = !!userName; 


  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home userName={userName} setUserName={setUserName} />} />
          <Route path="/login" element={<Login setUserName={setUserName} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/create-quiz" element={<ProtectedRoute isLoggedIn={isLoggedIn}><CreateQuiz /></ProtectedRoute>} />
          <Route path="/quizzes" element={<ProtectedRoute isLoggedIn={isLoggedIn}><Quizzes /></ProtectedRoute>} />
          <Route path="/quiz" element={<QuizPage userName={userName} />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;