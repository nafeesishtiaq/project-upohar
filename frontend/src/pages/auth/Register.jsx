import { useState } from "react";
import api from "../../api/api";
import { GoogleLogin } from "@react-oauth/google";

export default function Register() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("auth/register/", form);
      alert("Account created. You can log in now.");
      window.location.href = "/login";
    } catch (err) {
      setError("Registration failed");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded shadow w-80"
      >
        <h2 className="text-2xl font-bold mb-4 text-center">Register</h2>

        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}

        <input
          name="email"
          type="email"
          placeholder="Email"
          className="w-full mb-3 p-2 border rounded"
          onChange={handleChange}
          required
        />

        <input
          name="password"
          type="password"
          placeholder="Password"
          className="w-full mb-4 p-2 border rounded"
          onChange={handleChange}
          required
        />

        <button className="w-full bg-black text-white py-2 rounded mb-3">
          Sign up
        </button>

        <div className="text-center text-sm text-gray-500 mb-3">or</div>

        <GoogleLogin
          onSuccess={async (credentialResponse) => {
            try {
              const res = await api.post("auth/google/", {
                id_token: credentialResponse.credential,
              });

              localStorage.setItem("access", res.data.access);
              localStorage.setItem("refresh", res.data.refresh);

              alert("Signed up with Google");
              window.location.href = "/";
            } catch {
              setError("Google signup failed");
            }
          }}
          onError={() => setError("Google signup failed")}
        />
      </form>
    </div>
  );
}
