import React, { useState } from 'react'
import axios from 'axios'

function App() {
  const [resumeText, setResumeText] = useState('')
  const [jobText, setJobText] = useState('')
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const analyze = async () => {
    setLoading(true)
    try {
      const resp = await axios.post('/api/analyze', { resume: resumeText, job: jobText })
      setResult(resp.data)
    } catch (e) {
      setResult({ error: 'Failed to analyze' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app container">
      <header>
        <h1>AI Career Navigator (Demo)</h1>
        <p className="muted">Mocked analysis — no external AI service required</p>
      </header>

      <main>
        <section className="panel">
          <h2>Upload / Paste Resume</h2>
          <textarea value={resumeText} onChange={e => setResumeText(e.target.value)} rows={8} />
        </section>

        <section className="panel">
          <h2>Paste Job Description</h2>
          <textarea value={jobText} onChange={e => setJobText(e.target.value)} rows={6} />
        </section>

        <div style={{marginTop:12}}>
          <button className="btn" onClick={analyze} disabled={loading}>Analyze</button>
        </div>

        {loading && <p>Analyzing...</p>}

        {result && (
          <section className="panel">
            <h3>Results</h3>
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </section>
        )}
      </main>

      <footer className="muted">Demo backend provides mocked match scores, gaps, and questions.</footer>
    </div>
  )
}

export default App
