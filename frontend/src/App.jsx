import { useState } from 'react';
import CampaignPlanner from './components/CampaignPlanner';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <header className="header">
        <h1 className="title">AI Marketing Manager</h1>
        <p className="subtitle">Automate your entire marketing strategy with autonomous AI agents</p>
      </header>

      <main>
        <CampaignPlanner />
      </main>
    </div>
  );
}

export default App;
