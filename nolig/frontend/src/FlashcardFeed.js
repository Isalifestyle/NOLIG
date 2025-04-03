import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const FlashcardFeed = () => {
    const [flashcardSets, setFlashcardSets] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/flashcard_sets/")
            .then(response => setFlashcardSets(response.data))
            .catch(error => console.error("Error fetching flashcard sets:", error));
    }, []);

    return (
        <div>
            <h2>Flashcard Sets</h2>
            {flashcardSets.length > 0 ? (
                flashcardSets.map(set => (
                    <div key={set.id} className="flashcard-set">
                        <h3>
                            <Link to={`/flashcards/${set.id}`}>
                                {set.title}
                            </Link>
                        </h3>
                        <p>{set.description}</p>
                    </div>
                ))
            ) : (
                <p>No flashcard sets available.</p>
            )}
        </div>
    );
};

export default FlashcardFeed;
