import { api } from "./api";
export default function Register() {
  async function submit(e) {
    e.preventDefault();
    await api("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        email: e.target.email.value,
        password: e.target.password.value,
      }),
    });
    alert("Registered — login now");
  }

  return (
    <form onSubmit={submit}>
      <h2>Register</h2>
      <input name="email" />
      <input name="password" type="password" />
      <button>Register</button>
    </form>
  );
}
