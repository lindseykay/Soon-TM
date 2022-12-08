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

  function switchTab(event, val) {
    event.preventDefault();
    setMode(val);
    const tabs = document.querySelectorAll(".login-widget-tab");
    for (let node of tabs) {
      node.classList.remove("selected-tab");
    }
    const tab = document.querySelector(`#login-tab-${val}`);
    tab.classList.add("selected-tab");
  }

  return (
    <>
      {!landing && (
        <button className="login-button" onClick={(e) => setLanding(true)}>
          login / sign up
        </button>
      )}
      {landing && (
        <div className="login-widget-container">
          <div
            className="login-widget-tab selected-tab"
            id="login-tab-0"
            onClick={(e) => switchTab(e, 0)}
          >
            login
          </div>
          <div
            className="login-widget-tab"
            id="login-tab-1"
            onClick={(e) => switchTab(e, 1)}
          >
            sign up
          </div>
          <div className="form-input">
            <input
              required
              placeholder="username"
              type="text"
              className="form-option"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
            />
          </div>
          <div className="form-input">
            <input
              required
              placeholder="password"
              type="password"
              id="pass-box"
              className="form-option"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          {mode === 1 && (
            <>
              <div className="form-input">
                <input
                  required
                  placeholder="email"
                  type="text"
                  className="form-option"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div className="form-input">
                <input
                  required
                  placeholder="full name"
                  type="text"
                  className="form-option"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
            </>
          )}
          <div className="login-widget-footer">
            <div className="show-pass">
              <input type="checkbox" onClick={(e) => showPass(e)} />
              <span>Show Password</span>
            </div>
            <button
              className="form-submit"
              onClick={(e) => {
                mode === 0
                  ? login(userName, password)
                  : signup(userName, password, email, name);
              }}
            >
              {mode === 0 ? "login" : "sign up"}
            </button>
          </div>
          <div
            className="delete-mark"
            onClick={(e) => {
              setLanding(false);
              setMode(0);
              setUserName("");
              setPassword("");
              setEmail("");
              setName("");
            }}
          >
            <div className="x-mark">x</div>
          </div>
        </div>
      )}
    </>
  );
}

export default LoginWidget;
