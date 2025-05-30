import { useState } from 'react';

export const Analyzer = () => {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState<any>(null);

  const handleAnalyze = async () => {
    const response = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: inputText }),
    });
    const data = await response.json();
    setResult(data.result);
  };

  return (
    <div className="p-4">
      <textarea
        className="w-full p-2 border"
        rows={5}
        placeholder="Digite a URL ou texto para analisar..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      ></textarea>
      <button onClick={handleAnalyze} className="mt-2 px-4 py-2 bg-blue-500 text-white">
        Analisar
      </button>
      {result && (
        <div className="mt-4">
          <h2 className="font-bold">Resultado:</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};
