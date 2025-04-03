import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FlashcardList from './FlashcardList'; // Component that displays flashcards

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<FlashcardFeed />} />
                <Route path="/flashcards/:setId" element={<FlashcardList />} />
            </Routes>
        </Router>
    );
}

export default App;