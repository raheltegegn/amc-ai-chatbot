# AMC AI Chatbot

A modern, bilingual chatbot interface for Amhara Media Corporation (AMC) that provides news updates and institutional information in both Amharic and English.

## Features

- 🌍 Bilingual Support (Amharic/English)
- 🎙️ Voice Input Capability
- 📱 Responsive Design (Mobile/Desktop)
- 📰 Real-time News Updates
- 🏢 Institutional Information
- 🎨 Modern UI with AMC Branding
- ⚡ Real-time Response
- 🔄 Automatic Language Detection

## Tech Stack

### Frontend
- **Framework**: React.js
- **Styling**: TailwindCSS
- **State Management**: React Hooks
- **Voice Input**: Web Speech API
- **HTTP Client**: Native Fetch API

### Backend
- **Runtime**: Node.js
- **Framework**: Express.js
- **API Architecture**: RESTful
- **Language Processing**: Natural Language Processing (NLP)

## Project Structure

```
amc-ai-chatbot/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── Layout.jsx
│   │   │   └── VoiceInput.jsx
│   │   ├── config.js
│   │   ├── App.jsx
│   │   └── styles/
│   └── public/
└── backend/
    ├── routes/
    ├── services/
    └── server.js
```

## Key Components

### ChatInterface
- Main chat interface component
- Handles message history
- Manages API communication
- Implements error handling
- Provides bilingual support

### VoiceInput
- Voice recognition implementation
- Language-specific voice input
- Error handling for unsupported browsers
- Visual feedback during recording

### Layout
- Responsive layout implementation
- AMC branding integration
- Header with logo
- Mobile-friendly design

## Features in Detail

### 1. Bilingual Support
- Seamless switching between Amharic and English
- Language-specific responses
- Automatic language detection for voice input

### 2. News Integration
- Real-time news fetching
- Categorized news display
- Support for both Amharic and English news
- Click-through to full articles

### 3. Voice Recognition
- Browser-native speech recognition
- Language-specific voice input
- Real-time transcription
- Error handling for unsupported browsers

### 4. Responsive Design
- Mobile-first approach
- Adaptive layout
- Touch-friendly interface
- Cross-browser compatibility

### 5. Error Handling
- Network error detection
- Reconnection capability
- User-friendly error messages
- Graceful degradation



## Environment Variables

Create `.env` files in both frontend and backend directories:

Frontend (.env):
```
REACT_APP_API_URL=http://localhost:5000
```

Backend (.env):
```
PORT=5000
NODE_ENV=development
```

## Dependencies

### Frontend
- react
- react-dom
- tailwindcss
- @heroicons/react
- postcss
- autoprefixer

### Backend
- express
- cors
- dotenv
- body-parser

## Development Tools

- VS Code
- Node.js
- npm/yarn
- Git
- Chrome DevTools

## Challenges Faced and Solutions

1. **Mobile Responsiveness**
   - Challenge: Initial interface not working on mobile devices
   - Solution: Implemented responsive design patterns and proper API URL handling

2. **Voice Input Compatibility**
   - Challenge: Voice input not working on all browsers
   - Solution: Added fallback mechanisms and clear error messages

3. **Network Connectivity**
   - Challenge: Unstable connections causing chat failures
   - Solution: Implemented robust error handling and reconnection logic

4. **Bilingual Support**
   - Challenge: Handling both Amharic and English content
   - Solution: Implemented language-specific handlers and UI elements

## Future Improvements

1. **Offline Support**
   - Implement service workers
   - Add offline message queue

2. **Enhanced Security**
   - Add rate limiting
   - Implement request validation

3. **Performance Optimization**
   - Message caching
   - Image optimization
   - Code splitting

4. **Additional Features**
   - File sharing
   - Rich media support
   - User preferences storage

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments

- Amhara Media Corporation for the opportunity
- The open-source community for various tools and libraries
- Contributors and testers who helped improve the project
