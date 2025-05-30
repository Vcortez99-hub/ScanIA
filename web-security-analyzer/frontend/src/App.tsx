import { useState } from 'react';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState('');

  const apiUrl = import.meta.env.VITE_API_URL;

  const handleAnalyze = async () => {
    try {
      const response = await fetch(`${apiUrl}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }), // ✅ Alterado para "text"
      });

      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      console.error('Erro ao analisar:', error);
      setResult('Erro ao analisar o texto');
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>Web Security Analyzer</h1>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Digite o texto para análise"
        rows={5}
        style={{ padding: '0.5rem', width: '300px', marginRight: '1rem' }}
      />
      <br />
      <button
        onClick={handleAnalyze}
        style={{ padding: '0.5rem 1rem', marginTop: '1rem', cursor: 'pointer' }}
      >
        Analisar
      </button>

      <pre style={{ marginTop: '2rem', background: '#f4f4f4', padding: '1rem' }}>
        {result}
      </pre>
    </div>
  );
}

export default App;
