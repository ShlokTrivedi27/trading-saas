import { useEffect, useState } from "react";

export default function Dashboard() {
  const [signals, setSignals] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/signals", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => res.json())
      .then((data) => setSignals(data.signals || []));
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6">📈 Trading Signals</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {signals.map((s, i) => (
          <div
            key={i}
            className="bg-gray-800 p-4 rounded-lg flex justify-between items-center"
          >
            <span className="text-lg font-semibold">{s.symbol}</span>
            <span
              className={`font-bold ${
                s.action === "BUY" ? "text-green-400" : "text-red-400"
              }`}
            >
              {s.action}
            </span>
          </div>
        ))}
      </div>

      {signals.length === 0 && (
        <p className="text-gray-400 mt-4">No signals available</p>
      )}
    </div>
  );
}

