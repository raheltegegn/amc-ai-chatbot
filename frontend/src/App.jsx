import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import Layout from './components/Layout';
import './styles/App.css';

function App() {
  const [language, setLanguage] = useState('am');

  return (
    <Layout>
      <ChatInterface 
        language={language}
        onLanguageChange={setLanguage}
      />
    </Layout>
  );
}

export default App; 