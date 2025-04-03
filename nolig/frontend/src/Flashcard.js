// import React, { useState, useEffect } from "react";
// import { motion } from "framer-motion";
// import axios from "axios";
// import { useParams } from "react-router-dom";

// const Flashcard = ({ question, answer }) => {
//     const [flipped, setFlipped] = useState(false);

//     return (
//         <motion.div 
//             className="flashcard-container"
//             onClick={() => setFlipped(!flipped)}
//         >
//             <motion.div 
//                 className="flashcard"
//                 animate={{ rotateX: flipped ? 180 : 0 }} 
//                 transition={{ duration: 0.5 }}
//             >
//                 <div className="flashcard-face front">
//                     {question}
//                 </div>
//                 <div className="flashcard-face back">
//                     {answer}
//                 </div>
//             </motion.div>
//         </motion.div>
//     );
// };

// const FlashcardList = () => {
//     const { setId } = useParams(); // Get setId from URL
//     const [flashcards, setFlashcards] = useState([]);
//     const [currentIndex, setCurrentIndex] = useState(0);

//     useEffect(() => {
//         axios.get(`http://127.0.0.1:8000/api/flashcards/${setId}/`)
//             .then(response => {
//                 setFlashcards(response.data);
//             })
//             .catch(error => console.error("Error fetching flashcards:", error));
//     }, [setId]);

//     const nextCard = () => setCurrentIndex((prev) => (prev + 1) % flashcards.length);
//     const prevCard = () => setCurrentIndex((prev) => (prev - 1 + flashcards.length) % flashcards.length);

//     return (
//         <div className="flashcard-wrapper">
//             {flashcards.length > 0 ? (
//                 <>
//                     <Flashcard 
//                         question={flashcards[currentIndex].question} 
//                         answer={flashcards[currentIndex].answer} 
//                     />
//                     <p className="flashcard-counter">
//                         {currentIndex + 1} / {flashcards.length}
//                     </p>
//                     <div className="navigation-buttons">
//                         <button onClick={prevCard}>⬅️</button>
//                         <button onClick={nextCard}>➡️</button>
//                     </div>
//                 </>
//             ) : (
//                 <p>No flashcards available.</p>
//             )}
//         </div>
//     );
// };

// export default FlashcardList;
