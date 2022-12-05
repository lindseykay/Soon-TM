import { useToken } from "./hooks/useToken";
import LoginWidget from "./loginWidget";
import React from "react";
import { stack as Menu } from "react-burger-menu";

function NavBar() {
  const [token, , logout] = useToken();

  return (
    <div className="nav-bar">
      {!token && <LoginWidget />}
      {token && (
        <>
          <button className="logout-button" onClick={(e) => logout()}>Log out</button>
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
        <a className="menu-item" href="/">
          Settings
        </a>
      </Menu>
    </div>
  );
}

export default NavBar;
