import { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
let internalToken = null;
let userInfo = null;

export function getToken() {
  return internalToken;
}

export async function getTokenInternal() {
  const url = `${process.env.REACT_APP_ACCOUNTS_HOST}/token/`;
  try {
    const response = await fetch(url, {
      credentials: "include",
    });
    if (response.ok) {
      const data = await response.json();
      internalToken = data.access_token;
      userInfo = data.account
      return internalToken;
    }
  } catch (e) {}
  return false;
}

function handleErrorMessage(error) {
  if ("error" in error) {
    error = error.error;
    try {
      error = JSON.parse(error);
      if ("__all__" in error) {
        error = error.__all__;
      }
    } catch {}
  }
  if (Array.isArray(error)) {
    error = error.join("<br>");
  } else if (typeof error === "object") {
    error = Object.entries(error).reduce(
      (acc, x) => `${acc}<br>${x[0]}: ${x[1]}`,
      ""
    );
  }
  return error;
}

export const AuthContext = createContext({
  token: null,
  setToken: () => null,
});

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(null);

  return (
    <AuthContext.Provider value={{ token, setToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = () => useContext(AuthContext);

export function useToken() {
  const { token, setToken } = useAuthContext();
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchToken() {
      const token = await getTokenInternal();
      setToken(token);
    }
    if (!token) {
      fetchToken();
    }
  }, [setToken, token]);

  async function logout() {
    if (token) {
      const url = `${process.env.REACT_APP_ACCOUNTS_HOST}/token/`;
      await fetch(url, { method: "delete", credentials: "include" });
      internalToken = null;
      setToken(null);
      navigate("/reminders/new");
    }
  }

  async function login(username, password) {
    const url = `${process.env.REACT_APP_ACCOUNTS_HOST}/token/`;
    const form = new FormData();
    form.append("username", username);
    form.append("password", password);
    const response = await fetch(url, {
      method: "post",
      credentials: "include",
      body: form,
    });
    if (response.ok) {
        const token = await getTokenInternal();
        setToken(token);
        return;
    }
    let error = await response.json();
    return handleErrorMessage(error);
  }

  async function signup(username, password, email, name) {
    const url = `${process.env.REACT_APP_ACCOUNTS_HOST}/users/`;
    const response = await fetch(url, {
      method: "post",
      body: JSON.stringify({
        username,
        password,
        email,
        name
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (response.ok) {
      await login(username, password);
    }
    return false;
  }

  async function update(password, email, name) {
    const url = `${process.env.REACT_APP_ACCOUNTS_HOST}/users/`;
    // if (password === ""){
    //   var body = JSON.stringify({
    //     email,
    //     name
    //   })
    // } else {
    //    body = JSON.stringify({
    //     password,
    //     email,
    //     name
    //   })
    // };


    const response = await fetch(url, {
      method: "put",
      credentials: "include",
      body: JSON.stringify({
        password: password ? password : null,
        email: email,
        name: name ? name : null
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (response.ok) {
      await logout();
    }
    return false;
  }
  return [token, login, logout, signup, update, userInfo];
}
