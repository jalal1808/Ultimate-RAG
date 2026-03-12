import React, { useState, useRef } from 'react';
import axios from 'axios';

function App() {
  const [fileId, setFileId] = useState(null);
  const [fileName, setFileName] = useState('');
  const [summary, setSummary] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [isSummarizing, setIsSummarizing] = useState(false);
  const [isAsking, setIsAsking] = useState(false);
  const [error, setError] = useState(null);
  
  const fileInputRef = useRef(null);

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsUploading(true);
    setError(null);
    setFileName(file.name);
    setSummary('');
    setAnswer('');
    setQuestion('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setFileId(response.data.file_id);
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleSummarize = async () => {
    if (!fileId) return;
    setIsSummarizing(true);
    setError(null);
    try {
      const response = await axios.post('/api/summarize', { file_id: fileId });
      setSummary(response.data.summary);
    } catch (err) {
      setError(err.response?.data?.detail || 'Summarization failed.');
    } finally {
      setIsSummarizing(false);
    }
  };

  const handleAsk = async () => {
    if (!fileId || !question.trim()) return;
    setIsAsking(true);
    setError(null);
    try {
      const response = await axios.post('/api/ask', { 
        file_id: fileId, 
        question: question.trim() 
      });
      setAnswer(response.data.answer);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get an answer.');
    } finally {
      setIsAsking(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>UltimateRAG</h1>
        <p className="subtitle">Modern Document Intelligence for Text & Tables</p>
      </header>

      <div className="card">
        {!fileId ? (
          <div 
            className="upload-area" 
            onClick={() => fileInputRef.current.click()}
          >
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleUpload} 
              style={{ display: 'none' }}
              accept=".pdf,.docx,.txt,.md,.csv,.xlsx"
            />
            <p>{isUploading ? 'Uploading your document...' : 'Click to upload a document'}</p>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
              PDF, DOCX, TXT, MD, CSV, or XLSX
            </p>
          </div>
        ) : (
          <div>
            <div className="flex-between" style={{ marginBottom: '1.5rem' }}>
              <div>
                <span className="badge">Active Document</span>
                <h3 style={{ marginTop: '0.5rem' }}>{fileName}</h3>
              </div>
              <button 
                className="btn btn-outline" 
                onClick={() => { setFileId(null); setFileName(''); setSummary(''); setAnswer(''); }}
              >
                Clear
              </button>
            </div>

            <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
              <button 
                className="btn btn-primary" 
                onClick={handleSummarize}
                disabled={isSummarizing}
              >
                {isSummarizing ? <span className="loading-dots">Summarizing</span> : 'Summarize Document'}
              </button>
            </div>
          </div>
        )}

        {error && (
          <div style={{ color: '#ef4444', marginTop: '1rem', fontSize: '0.9rem', textAlign: 'center' }}>
            {error}
          </div>
        )}
      </div>

      {summary && (
        <div className="card">
          <h4>Summary</h4>
          <div className="result-box">{summary}</div>
        </div>
      )}

      {fileId && (
        <div className="card">
          <h4>Ask a Question</h4>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1rem' }}>
            Query the document using natural language.
          </p>
          <div className="input-group">
            <input 
              type="text" 
              placeholder="Who is the primary contact? What are the key takeaways?" 
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAsk()}
            />
            <button 
              className="btn btn-primary" 
              onClick={handleAsk}
              disabled={isAsking || !question.trim()}
            >
              {isAsking ? <span className="loading-dots">Thinking</span> : 'Ask'}
            </button>
          </div>

          {answer && (
            <div className="result-box" style={{ background: '#fefce8', borderColor: '#fef08a' }}>
              <strong>Answer:</strong>
              <div style={{ marginTop: '0.5rem' }}>{answer}</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
