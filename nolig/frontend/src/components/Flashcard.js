// import React, { useState } from "react";
// import { motion } from "framer-motion";
// import "../styles/flashcards.css"; // Import CSS for styling

// const Flashcard = ({ question, answer }) => {
//     const [flipped, setFlipped] = useState(false);

//     return (
//         <motion.div 
//             className="flashcard-container"
//             onClick={() => setFlipped(!flipped)}
//         >
//             <motion.div 
//                 className="flashcard"
//                 animate={{ rotateX: flipped ? 180 : 0 }} // Flip from top to bottom
//                 transition={{ duration: 0.5 }}
//             >
//                 {/* Front Side */}
//                 <div className="flashcard-face front">
//                     {question}
//                 </div>
                
//                 {/* Back Side */}
//                 <div className="flashcard-face back">
//                     {answer}
//                 </div>
//             </motion.div>
//         </motion.div>
//     );
// };

// export default Flashcard;
