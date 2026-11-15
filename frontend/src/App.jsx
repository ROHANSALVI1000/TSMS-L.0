import { useState } from "react";

import {
    Routes,
    Route,
    Navigate
} from "react-router-dom";

import Login from "./Login";
import Dashboard from "./Dashboard";


function App() {

    const [token, setToken] = useState("");

    return (
        <Routes>

            <Route
                path="/"
                element={
                    <Login
                        setToken={setToken}
                    />
                }
            />

            <Route
                path="/dashboard"
                element={
                    token
                    ? <Dashboard
                        token={token}
                        setToken={setToken}
                      />
                    : <Navigate to="/" replace />
                }
            />

        </Routes>
    );
}

export default App;