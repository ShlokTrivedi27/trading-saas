import { useNavigate } from "react-router-dom";

function Subscribe() {
  const navigate = useNavigate(); 

  return (
    <div style={{ padding: "40px", textAlign: "center" }}>
      <h1>Upgrade to Pro</h1>

      <button
        style={{
          padding: "12px 24px",
          fontSize: "16px",
          marginTop: "20px",
          cursor: "pointer",
        }}
      >
        Upgrade ₹999/month
      </button>

      <p style={{ marginTop: "20px" }}>
        Already have an account?{" "}
        <span
          onClick={() => navigate("/")}  // ✅ NO login variable
          style={{ color: "#2563eb", cursor: "pointer" }}
        >
          Login
        </span>
      </p>
    </div>
  );
}

export default Subscribe;
