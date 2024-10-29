import React from 'react';
import RaceNode from './RaceNode';

const RaceTree = ({ root }) => {
  return (
    <div>
      <h1>Race Outcome Tree</h1>
      {root && <RaceNode node={root} />}
    </div>
  );
};

export default RaceTree;
