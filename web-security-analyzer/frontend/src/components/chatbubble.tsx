import React from "react";

type Props = {
  message: string;
  isUser: boolean;
};

const ChatBubble: React.FC<Props> = ({ message, isUser }) => {
  return (
    <div className={`my-2 flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`p-3 rounded-2xl max-w-xs ${isUser ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}>
        {message}
      </div>
    </div>
  );
};

export default ChatBubble;
