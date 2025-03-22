import React, { useState, useEffect } from "react";
import axios from "axios";
import Flashcard from "./Flashcard"; // Ensure you import your Flashcard component
import "../styles/flashcards.css"; // Import CSS for styling

const FlashcardList = () => {
    const [flashcards, setFlashcards] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);

    // Fetch flashcards from API
    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/flashcards/")
            .then(response => {
                const formattedFlashcards = response.data.map(card => ({
                    id: card.id,
                    question: card.question,
                    answer: card.answer
                }));
                setFlashcards(formattedFlashcards);
            })
            .catch(error => console.error("Error fetching flashcards:", error));
    }, []);

    // Handle navigation
    const nextCard = () => {
        setCurrentIndex((prev) => (prev + 1) % flashcards.length);
    };

    const prevCard = () => {
        setCurrentIndex((prev) => (prev - 1 + flashcards.length) % flashcards.length);
    };

    return (
        <div className="flashcard-wrapper">
            <button onClick={prevCard} disabled={flashcards.length === 0}>⬅️</button>
            {flashcards.length > 0 ? (
                <Flashcard 
                    question={flashcards[currentIndex].question} 
                    answer={flashcards[currentIndex].answer} 
                />
            ) : (
                <p>Loading flashcards...</p>
            )}
            <button onClick={nextCard} disabled={flashcards.length === 0}>➡️</button>
        </div>
    );
};

export default FlashcardList;
