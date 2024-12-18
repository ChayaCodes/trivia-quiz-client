import React, { useState, useEffect } from "react";
import "./Quizzes.css";

function Quizzes() {
  const [quizzes, setQuizzes] = useState([]);

  useEffect(() => {
    const fetchQuizzes = async () => {
      const data = [
        {
          id: 1,
          title: "החידון הראשון",
          description: "חידון ראשון עם תיאור קצר",
        },
        {
          id: 2,
          title: "החידון השני",
          description: "חידון שני עם תיאור קצר",
        },
        {
          id: 3,
          title: "החידון השלישי",
          description: "חידון שלישי עם תיאור קצר",
        },
      ];
      setQuizzes(data);
    };

    fetchQuizzes();
  }, []);

  return (
    <div>
      <h1 className="Title">רשימת החידונים</h1>
      <ul className="quiz-list">
        {quizzes.map((quiz) => (
          <li className="quiz-item" key={quiz.id}>
            <h2>{quiz.title}</h2>
            <p>{quiz.description}</p>
            <div className="buttons">
              <button className="activate-button">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  height="24"
                  width="20.5"
                  viewBox="0 0 384 512"
                >
                  <path
                    fill="#000000"
                    d="M73 39c-14.8-9.1-33.4-9.4-48.5-.9S0 62.6 0 80L0 432c0 17.4 9.4 33.4 24.5 41.9s33.7 8.1 48.5-.9L361 297c14.3-8.7 23-24.2 23-41s-8.7-32.2-23-41L73 39z"
                  />
                </svg>
              </button>
                <button className="edit-button">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    height="24"
                    width="24"
                    viewBox="0 0 512 512"
                  >
                    <path
                      fill="#000000"
                      d="M471.6 21.7c-21.9-21.9-57.3-21.9-79.2 0L362.3 51.7l97.9 97.9 30.1-30.1c21.9-21.9 21.9-57.3 0-79.2L471.6 21.7zm-299.2 220c-6.1 6.1-10.8 13.6-13.5 21.9l-29.6 88.8c-2.9 8.6-.6 18.1 5.8 24.6s15.9 8.7 24.6 5.8l88.8-29.6c8.2-2.7 15.7-7.4 21.9-13.5L437.7 172.3 339.7 74.3 172.4 241.7zM96 64C43 64 0 107 0 160L0 416c0 53 43 96 96 96l256 0c53 0 96-43 96-96l0-96c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 96c0 17.7-14.3 32-32 32L96 448c-17.7 0-32-14.3-32-32l0-256c0-17.7 14.3-32 32-32l96 0c17.7 0 32-14.3 32-32s-14.3-32-32-32L96 64z"
                    />
                  </svg>
                </button>
              <button className="delete-button">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  height="24"
                  width="22.25"
                  viewBox="0 0 448 512"
                >
                  <path
                    fill="#000000"
                    d="M135.2 17.7L128 32 32 32C14.3 32 0 46.3 0 64S14.3 96 32 96l384 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-96 0-7.2-14.3C307.4 6.8 296.3 0 284.2 0L163.8 0c-12.1 0-23.2 6.8-28.6 17.7zM416 128L32 128 53.2 467c1.6 25.3 22.6 45 47.9 45l245.8 0c25.3 0 46.3-19.7 47.9-45L416 128z"
                  />
                </svg>
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Quizzes;
