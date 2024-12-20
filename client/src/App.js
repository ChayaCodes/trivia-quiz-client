import "./App.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Home from "./pages/HomePage/HomePage";
import Login from "./pages/LoginForm/LoginForm";
import Register from "./pages/RegisterForm/RegisterForm";
import CreateQuiz from "./pages/CreateQuiz/CreateQuiz";
import QuizPage from "./pages/QuizPage/QuizPage";
import Quizzes from "./pages/Quizzes/Quizzes";
import Layout from "./components/Layout/Layout";

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/create-quiz" element={<CreateQuiz />} />
          <Route path="/quiz/:quizId" element={<QuizPage />} /> 
          <Route path="/quizzes" element={<Quizzes />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;