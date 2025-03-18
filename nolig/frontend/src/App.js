import React from "react";
import FlashcardList from "./Flashcard"; // Import the FlashcardList component
import "./styles/flashcards.css";


function App() {
  return (
    <div className="App">
      <h1>Flashcards</h1>
      <FlashcardList />
    </div>
  );
}

export default App;