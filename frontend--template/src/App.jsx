import {useState} from "react";

function app(){

    const[name,setname]=useState("");
    const[pas,setpas]=useState("");
    const[message,setmessage]=useState("");
    const[token,settoken]=useState("");



    async function handleLogin(event) {
        event.preventDefault();


        try{
            const response=await fetch(
                "http://localhost:8000/login",
                {
                    method:"POST",
                    headers:{
                        "content-type":"application/json"
                    },
                    body:JSON.stringify({name,pas})
                }
            );
            const data= await response.json();
         if (!response.ok){
              throw new Error(data.detail||"failed")
              }

          settoken(data.access_token)
          setmessage(data.message);


      
        }

        catch (error){
            setmessage(error.message)
        }
        
    }
    return(
        <div>
            <h2>login form</h2>
            <form onSubmit={handleLogin}>
                <input
                type="text"
                placeholder="name"
                value={name}
                onChange={(e) => setname(e.target.value)}
                /><required></required><br></br>

                <input
                type="password"
                placeholder="password"
                value={pas}
                onChange={(e) => setpas(e.target.value)}
                /><required></required><br></br>

                <button type="submit">login</button>
               
            </form>

            <p>{message}</p>
            {token && (
                <p>JWT successfully received!</p>
            )}
        </div>

    );
}
export default app;