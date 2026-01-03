const API_BASE_URL = 'http://localhost:8000'

async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  }

  try {
    const response = await fetch(url, config)

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'An error occurred')
    }

    return await response.json()
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
}

export const api = {
  // Get all papers
  getPapers: () => fetchAPI('/papers/'),

  // Get single paper
  getPaper: (id) => fetchAPI(`/papers/${id}`),

  // Create paper
  createPaper: (paper) =>
    fetchAPI('/papers/', {
      method: 'POST',
      body: JSON.stringify(paper),
    }),

  // Update paper
  updatePaper: (id, paper) =>
    fetchAPI(`/papers/${id}`, {
      method: 'PUT',
      body: JSON.stringify(paper),
    }),

  // Delete paper
  deletePaper: (id) =>
    fetchAPI(`/papers/${id}`, {
      method: 'DELETE',
    }),

  // Search OpenAlex
  searchOpenAlex: (query, limit = 10) =>
    fetchAPI('/search', {
      method: 'POST',
      body: JSON.stringify({ query, limit }),
    }),

  // Add paper from OpenAlex
  addFromOpenAlex: (openalex_id, notes = '') =>
    fetchAPI('/papers/from-openalex', {
      method: 'POST',
      body: JSON.stringify({ openalex_id, notes }),
    }),
}
