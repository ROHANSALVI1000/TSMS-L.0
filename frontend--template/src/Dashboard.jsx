import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";


function Dashboard({ token, setToken }) {

    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState("");

    const navigate = useNavigate();


    useEffect(() => {

        async function getDashboard() {

            try {

                const response = await fetch(
                    "http://localhost:8000/dashboard",
                    {
                        method: "GET",

                        headers: {
                            "Authorization": `Bearer ${token}`
                        }
                    }
                );

                const data = await response.json();

                if (!response.ok) {

                    throw new Error(
                        data.detail || "Failed to load dashboard"
                    );

                }

                setUser(data);

            }

            catch (error) {

                setMessage(error.message);

                // If authentication fails, return to login
                setToken("");

                navigate("/");

            }

            finally {

                setLoading(false);

            }
        }

        getDashboard();

    }, [token, setToken, navigate]);


    if (loading) {
        return <h2>Loading dashboard...</h2>;
    }


    if (!user) {
        return <p>{message}</p>;
    }


    return (

        <div>

            <h1>Welcome, {user.name}</h1>

            <p>User ID: {user.user_id}</p>

            <p>{user.message}</p>

        </div>

    );

}

export default Dashboard;