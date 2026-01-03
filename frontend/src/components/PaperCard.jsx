import './PaperCard.css'

function PaperCard({ paper }) {
  return (
    <div className="paper-card">
      <h3 className="paper-title">{paper.title}</h3>

      <div className="paper-meta">
        {paper.authors && (
          <p className="paper-authors">
            <strong>Authors:</strong> {paper.authors}
          </p>
        )}
        {paper.year && (
          <p className="paper-year">
            <strong>Year:</strong> {paper.year}
          </p>
        )}
      </div>

      {paper.abstract && (
        <p className="paper-abstract">
          {paper.abstract.length > 300
            ? `${paper.abstract.substring(0, 300)}...`
            : paper.abstract}
        </p>
      )}

      {paper.notes && (
        <p className="paper-notes">
          <strong>Notes:</strong> {paper.notes}
        </p>
      )}

      {paper.url && (
        <a
          href={paper.url}
          target="_blank"
          rel="noopener noreferrer"
          className="paper-link"
        >
          View Paper →
        </a>
      )}
    </div>
  )
}

export default PaperCard
