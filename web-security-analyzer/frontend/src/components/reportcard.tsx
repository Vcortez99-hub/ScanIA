import React from "react";

type Props = {
  title: string;
  content: string;
};

const ReportCard: React.FC<Props> = ({ title, content }) => {
  return (
    <div className="p-4 border rounded-lg shadow my-2">
      <h3 className="font-bold text-lg">{title}</h3>
      <p className="text-gray-700">{content}</p>
    </div>
  );
};

export default ReportCard;
