import React, { useEffect, useState } from 'react';
import RaceTree from './components/RaceTree';

const App = () => {
  const [root, setRoot] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const eventSource = new EventSource('http://localhost:5000/api/get-tree');

    eventSource.onmessage = (event) => {
      const node = JSON.parse(event.data);
      setRoot((prevRoot) => {
        // If there is no root, set the first received node as the root
        if (!prevRoot) {
          return node; 
        }

        // Otherwise, find the correct position to add the new node
        const addNode = (currentNode) => {
          if (currentNode.max_points === node.max_points && currentNode.lando_points === node.lando_points) {
            currentNode.children.push(node); // Add to children if matching points
          } else {
            currentNode.children.forEach(addNode);
          }
        };

        addNode(prevRoot);
        return { ...prevRoot }; // Return a new object reference to trigger re-render
      });
    };

    eventSource.onerror = () => {
      console.error('Error in EventSource');
      eventSource.close(); // Close the connection on error
    };

    return () => {
      eventSource.close(); // Clean up the EventSource on component unmount
    };
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      {root ? <RaceTree root={root} /> : <div>No data available.</div>}
    </div>
  );
};

export default App;
