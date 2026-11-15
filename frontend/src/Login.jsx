import { useState } from "react";
import { useNavigate } from "react-router-dom";


function Login({ setToken }) {

    const [name, setName] = useState("");
    const [pas, setPas] = useState("");
    const [message, setMessage] = useState("");

    const navigate = useNavigate();


    async function handleLogin(event) {

        event.preventDefault();

        try {

            const response = await fetch(
                "http://localhost:8000/login",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        name,
                        pas
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Login failed"
                );
            }

            // Store JWT in parent App state
            setToken(data.access_token);

            setMessage(data.message);

            // Navigate to dashboard
            navigate("/dashboard");

        }

        catch (error) {

            setMessage(error.message);

        }
    }


    return (

        <div>

            <h2>Login</h2>

            <form onSubmit={handleLogin}>

                <input
                    type="text"
                    placeholder="Username"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />

                <br />

                <input
                    type="password"
                    placeholder="Password"
                    value={pas}
                    onChange={(e) => setPas(e.target.value)}
                    required
                />

                <br />

                <button type="submit">
                    Login
                </button>

            </form>

            <p>{message}</p>

        </div>

    );
}

export default Login;