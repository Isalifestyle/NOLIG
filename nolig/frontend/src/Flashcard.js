import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import axios from "axios";

const Flashcard = ({ question, answer }) => {
    const [flipped, setFlipped] = useState(false);

    return (
        <motion.div 
            className="flashcard-container"
            onClick={() => setFlipped(!flipped)}
        >
            <motion.div 
                className="flashcard"
                animate={{ rotateX: flipped ? 180 : 0 }} // Flip from top to bottom
                transition={{ duration: 0.5 }}
            >
                {/* Front Side */}
                <div className="flashcard-face front">
                    {question}
                </div>
                
                {/* Back Side */}
                <div className="flashcard-face back">
                    {answer}
                </div>
            </motion.div>
        </motion.div>
    );
};

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
            {flashcards.length > 0 ? (
                <>
                    <Flashcard 
                        question={flashcards[currentIndex].question} 
                        answer={flashcards[currentIndex].answer} 
                    />
                    {/* Flashcard Number Indicator */}
                    <p className="flashcard-counter">
                        {currentIndex + 1} / {flashcards.length}
                    </p>

                    {/* Navigation Buttons */}
                    <div className="navigation-buttons">
                        <button onClick={prevCard} disabled={flashcards.length === 0}>⬅️</button>
                        <button onClick={nextCard} disabled={flashcards.length === 0}>➡️</button>
                    </div>
                </>
            ) : (
                <p>Loading flashcards...</p>
            )}
        </div>
    );
};

export default FlashcardList;
