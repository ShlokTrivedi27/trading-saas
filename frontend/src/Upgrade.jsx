// src/Upgrade.jsx
import { api } from "./api";

export default function Upgrade() {
  async function upgrade() {
    const res = await api("/billing/create-checkout", { method: "POST" });
    window.location.href = res.url;
  }

  return <button onClick={upgrade}>Upgrade to Pro 💳</button>;
}
