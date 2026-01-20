import { useState } from "react";
import Login from "./Login";
import { getUser, logout } from "./Auth";

export default function App() {
  const [user, setUser] = useState(getUser());

  if (!user) {
    return <Login onLogin={setUser} />;
  }

  return (
    <div>
      <h1>Welcome {user.email}</h1>
      <button onClick={() => { logout(); setUser(null); }}>
        Logout
      </button>
    </div>
  );
}
