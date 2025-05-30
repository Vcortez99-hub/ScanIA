import React, { useState } from "react";

type Props = {
  onSend: (text: string) => void;
};

const InputBar: React.FC<Props> = ({ onSend }) => {
  const [text, setText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      onSend(text);
      setText("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex p-2 border-t">
      <input
        className="flex-grow p-2 border rounded-l-lg"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Digite a URL para análise..."
      />
      <button className="bg-blue-500 text-white px-4 rounded-r-lg" type="submit">
        Enviar
      </button>
    </form>
  );
};

export default InputBar;
