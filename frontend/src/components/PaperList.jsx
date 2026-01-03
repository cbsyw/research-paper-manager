import { useState, useEffect } from 'react'
import { api } from '../services/api'
import PaperCard from './PaperCard'
import './PaperList.css'

function PaperList() {
  const [papers, setPapers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadPapers()
  }, [])

  const loadPapers = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.getPapers()
      setPapers(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="paper-list-status">
        <div className="spinner"></div>
        <p>Loading papers...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="paper-list-status error">
        <p>Error: {error}</p>
        <button onClick={loadPapers} className="retry-button">
          Retry
        </button>
      </div>
    )
  }

  if (papers.length === 0) {
    return (
      <div className="paper-list-status">
        <p>No papers found. Add some papers to get started!</p>
      </div>
    )
  }

  return (
    <div className="paper-list">
      <div className="paper-list-header">
        <h2>Your Papers ({papers.length})</h2>
      </div>

      <div className="paper-grid">
        {papers.map((paper) => (
          <PaperCard key={paper.id} paper={paper} />
        ))}
      </div>
    </div>
  )
}

export default PaperList
