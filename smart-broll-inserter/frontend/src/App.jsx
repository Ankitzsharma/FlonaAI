import { useState } from 'react'
import axios from 'axios'
import './App.css'

const DEFAULT_METADATA = [
  {
    "id": "broll_1",
    "metadata": "Mumbai street food context shot with closed or empty stalls, utensils and signboards visible, no people present. Establishes everyday food culture in an urban Indian city."
  },
  {
    "id": "broll_2",
    "metadata": "Indoor shot of takeaway food containers placed on a table near a window, natural daylight, calm and relatable everyday eating scenario with no humans in frame."
  },
  {
    "id": "broll_3",
    "metadata": "Close-up of uncovered food kept at a stall counter, subtle dust particles visible in light, highlighting hygiene concerns in a realistic, non-dramatic way."
  },
  {
    "id": "broll_4",
    "metadata": "Clean indoor kitchen counter with freshly prepared food, vegetables and utensils neatly arranged, warm lighting showing a hygienic alternative."
  },
  {
    "id": "broll_5",
    "metadata": "Organized indoor cafe or restaurant food display area, clean surfaces and professional setup, no staff or customers visible, reinforcing conscious food choices."
  },
  {
    "id": "broll_6",
    "metadata": "Minimal indoor dining table near a window with a glass of water and fresh fruits, soft sunlight creating a calm, reflective closing shot focused on health."
  }
]

function App() {
  const [aRoll, setARoll] = useState(null)
  const [bRolls, setBRolls] = useState(null)
  const [metadata, setMetadata] = useState(JSON.stringify(DEFAULT_METADATA, null, 2))
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleGenerate = async () => {
    if (!aRoll || !bRolls) {
      alert("Please upload A-Roll and B-Rolls")
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('a_roll', aRoll)
    for (let i = 0; i < bRolls.length; i++) {
      formData.append('b_rolls', bRolls[i])
    }
    formData.append('b_rolls_metadata', metadata)

    try {
      const response = await axios.post('http://localhost:8000/generate-plan', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      setResult(response.data)
    } catch (err) {
      console.error(err)
      let errorMessage = "An error occurred";
      if (err.response) {
        // Server responded with a status code outside 2xx
        if (typeof err.response.data.detail === 'string') {
           errorMessage = err.response.data.detail;
        } else if (err.response.data.message) {
           errorMessage = err.response.data.message;
        } else {
           errorMessage = JSON.stringify(err.response.data);
        }
      } else if (err.message) {
        // Request setup error
        errorMessage = err.message;
      }
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header>
        <h1>Smart B-Roll Inserter</h1>
        <p>AI-Powered Video Editor for UGC</p>
      </header>

      <div className="upload-section">
        <div className="input-group">
          <label>1. Upload A-Roll (Talking Head)</label>
          <input type="file" accept="video/*" onChange={(e) => setARoll(e.target.files[0])} />
        </div>

        <div className="input-group">
          <label>2. Upload B-Rolls (Select 6 clips)</label>
          <input type="file" accept="video/*" multiple onChange={(e) => setBRolls(e.target.files)} />
        </div>

        <div className="input-group">
          <label>3. B-Roll Metadata (JSON)</label>
          <textarea 
            rows={10} 
            value={metadata} 
            onChange={(e) => setMetadata(e.target.value)} 
          />
        </div>

        <button 
          className="generate-btn" 
          onClick={handleGenerate} 
          disabled={loading}
        >
          {loading ? 'Processing...' : 'Generate B-Roll Plan'}
        </button>

        {error && <div className="error">{error}</div>}
      </div>

      {result && (
        <div className="results-section">
          <h2>Results</h2>
          
          <div className="result-block">
            <h3>Transcript</h3>
            <div className="transcript-box">
              {result.transcript.map((seg, i) => (
                <span key={i} title={`${seg.start.toFixed(1)}s - ${seg.end.toFixed(1)}s`}>
                  {seg.text} 
                </span>
              ))}
            </div>
          </div>

          <div className="result-block">
            <h3>Timeline Plan</h3>
            <table className="timeline-table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Duration</th>
                  <th>B-Roll ID</th>
                  <th>Reason</th>
                  <th>Confidence</th>
                </tr>
              </thead>
              <tbody>
                {result.insertions.map((item, i) => (
                  <tr key={i}>
                    <td>{item.start_sec.toFixed(1)}s</td>
                    <td>{item.duration_sec.toFixed(1)}s</td>
                    <td>{item.broll_id}</td>
                    <td>{item.reason}</td>
                    <td>{item.confidence}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {result.video_url && (
            <div className="result-block">
              <h3>Final Video</h3>
              <video controls src={`http://localhost:8000${result.video_url}`} width="100%" />
            </div>
          )}

          <div className="result-block">
            <h3>Raw JSON</h3>
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
