import { useToken } from "./hooks/useToken";
import LoginWidget from "./loginWidget";
import React from "react";
import { stack as Menu } from "react-burger-menu";
import { NavLink } from "react-router-dom";

function NavBar() {
  const [token, , logout] = useToken();

  return (
    <div className="nav-bar">
      {!token && <LoginWidget />}
      {token && (
        <>
          <button className="logout-button" onClick={(e) => logout()}>
            Log out
          </button>
        </>
      )}
      <Menu>
        <div className="menu-container">
          <NavLink className="menu-item" to="/">
            home
          </NavLink>
          {token && (
            <>
              <NavLink
                className={({ isActive }) =>
                  isActive ? "active-menu-item" : "menu-item"
                }
                to="/home/reminders/"
              >
                reminders
              </NavLink>
              <NavLink
                className={({ isActive }) =>
                  isActive ? "active-menu-item" : "menu-item"
                }
                to="/home/contacts/"
              >
                contacts
              </NavLink>
              <NavLink
                className={({ isActive }) =>
                  isActive ? "active-menu-item" : "menu-item"
                }
                to="/home/templates/"
              >
                templates
              </NavLink>
              <NavLink
                className={({ isActive }) =>
                  isActive ? "active-menu-item" : "menu-item"
                }
                to="/home/settings/"
              >
                settings
              </NavLink>
            </>
          )}
          <NavLink className="menu-item" to="/reminders/new/">
            create a new reminder
          </NavLink>
        </div>
      </Menu>
    </div>
  );
}

export default NavBar;
