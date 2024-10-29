import React from 'react';

const RaceNode = ({ node }) => {
  return (
    <div style={{ marginLeft: '20px' }}>
      <p>Race: {node.description ? node.description.type : 'N/A'}, Max Points: {node.max_points}, Lando Points: {node.lando_points}</p>
      {node.winning_path && <strong>Lando finishes ahead on this path!</strong>}
      {node.children && node.children.map((child, index) => (
        <RaceNode key={index} node={child} />
      ))}
    </div>
  );
};

export default RaceNode;
