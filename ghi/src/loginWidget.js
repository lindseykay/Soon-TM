import { useState } from "react";
import { useToken } from "./hooks/useToken";
import "./index.css";

function LoginWidget() {
  const [, login, , signup] = useToken();
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [mode, setMode] = useState(0);
  const [landing, setLanding] = useState(false);

  function showPass(e) {
    let passInput = document.getElementById("pass-box");
    passInput.type = passInput.type === "password" ? "text" : "password";
  }

  return (
    <div className="landing-container">
      {!landing && (
        <button onClick={(e) => setLanding(!landing)}>Login/Signup</button>
      )}
      {landing && (
        <div className="login-widget-container">
          <button onClick={(e) => setMode(0)}>Login</button>
          <button onClick={(e) => setMode(1)}>Signup</button>
          <input
            required
            placeholder="Username"
            type="text"
            className="form-option"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
          />
          <input
            required
            placeholder="Password"
            type="password"
            id="pass-box"
            className="form-option"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <input type="checkbox" onClick={(e) => showPass(e)} />
          <span className="show-pass">Show Password</span>
          {mode === 1 && (
            <>
              <input
                required
                placeholder="Email"
                type="text"
                className="form-option"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <input
                required
                placeholder="Name"
                type="text"
                className="form-option"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </>
          )}
          <button
            onClick={(e) => {
              mode === 0
                ? login(userName, password)
                : signup(userName, password, email, name);
            }}
          >
            {mode === 0 ? "Login" : "Sign up"}
          </button>
        </div>
      )}
    </div>
  );
}

export default LoginWidget;
