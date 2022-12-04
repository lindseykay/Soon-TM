import { useToken } from "./hooks/useToken";
import LoginWidget from "./loginWidget";
import { NavLink } from "react-router-dom";

import React from "react";
import { stack as Menu } from "react-burger-menu";
import "./Sidebar.css"; // Decide with team if we want to implement this into index.css to clean up directory

function NavBar() {
  const [token, , logout] = useToken();

  return (
    <div className="nav-bar">
      {!token && <LoginWidget />}
      {token && (
        <>
          <div>menu placeholder</div>
          <button onClick={(e) => logout()}>Log out</button>
        </>
      )}
      <Menu>
        <a className="menu-item" href="/">
          Home
        </a>
        <a className="menu-item" href="/">
          My Reminders
        </a>
        <a className="menu-item" href="/">
          My Contacts
        </a>
        <NavLink to="/home/settings" className={({isActive}) => (isActive ? "active-now": "inactive")}>
                <div className="dashboard-tabs">settings</div>
        </NavLink>
      </Menu>
    </div>
  );
}

export default NavBar;
