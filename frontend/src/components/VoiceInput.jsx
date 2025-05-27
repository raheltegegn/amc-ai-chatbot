import React, { useState } from 'react';

const VoiceInput = ({ onResult, language, disabled }) => {
  const [isListening, setIsListening] = useState(false);

  const startListening = () => {
    if (disabled) return;
    
    if (!('webkitSpeechRecognition' in window)) {
      alert(language === 'am' 
        ? 'የድምፅ ግብዓት በዚህ ብራውዘር አይደገፍም።' 
        : 'Voice input is not supported in this browser.');
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.lang = language === 'am' ? 'am-ET' : 'en-US';

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      onResult(transcript);
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
      
      // Show appropriate error message
      const errorMessage = language === 'am'
        ? 'የድምፅ ግብዓት ስህተት። እባክዎ እንደገና ይሞክሩ።'
        : 'Voice input error. Please try again.';
      alert(errorMessage);
    };

    recognition.start();
  };

  return (
    <button
      onClick={startListening}
      type="button"
      disabled={disabled}
      className={`p-3 rounded-xl transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 ${
        isListening 
          ? 'bg-red-600 text-white hover:bg-red-700' 
          : disabled
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
      }`}
      title={
        disabled
          ? (language === 'am' ? 'አይገኝም' : 'Not available')
          : (language === 'am' ? 'የድምፅ ግብዓት' : 'Voice Input')
      }
    >
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        className="h-6 w-6" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          strokeWidth={2} 
          d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" 
        />
      </svg>
    </button>
  );
};

export default VoiceInput; 