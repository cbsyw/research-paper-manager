import { useState, useEffect } from 'react'
import PaperList from './components/PaperList'
import './App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Research Paper Manager</h1>
      </header>
      <main className="app-main">
        <PaperList />
      </main>
    </div>
  )
}

export default App
