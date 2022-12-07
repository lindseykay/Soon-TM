import { useToken } from "../hooks/useToken";
import { Outlet } from "react-router-dom";
import { NavLink } from "react-router-dom";

function UserDashboard() {
  const [token, , , , , userInfo] = useToken();
  return (
    <>
      <div className="dash-greeting">
        Welcome back {userInfo ? userInfo.name.toUpperCase() : "USER"}!
      </div>
      <div className="dashboard-tabs">
        <NavLink
          to="soon-tm/home/reminders"
          className={({ isActive }) => (isActive ? "active-now" : "inactive")}
        >
          reminders
        </NavLink>
        <NavLink
          to="soon-tm/home/contacts"
          className={({ isActive }) => (isActive ? "active-now" : "inactive")}
        >
          contacts
        </NavLink>
        <NavLink
          to="soon-tm/home/templates"
          className={({ isActive }) => (isActive ? "active-now" : "inactive")}
        >
          templates
        </NavLink>
        {/* <NavLink to="soon-tm/home/settings" className={({isActive}) => (isActive ? "active-now": "inactive")}>
                    settings
                </NavLink> */}
      </div>
      <div className="sub-display">{token && <Outlet />}</div>
    </>
  );
}

export default UserDashboard;
