import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('/data')
      .then((res) => res.json())
      .then(setData);
  }, []);

  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h1>Shop Products</h1>
      {data.shops.map((shop) => (
        <div key={shop.id}>
          <h2>{shop.title}</h2>
          <ul>
            {shop.products.map((prod) => (
              <li key={prod.id}>{prod.title}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default App;
