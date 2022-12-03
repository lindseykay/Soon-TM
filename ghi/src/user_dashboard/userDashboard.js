import { useState, useEffect } from 'react'
import { useToken } from '../hooks/useToken'
import { Outlet } from 'react-router-dom'
import { NavLink } from 'react-router-dom'


function UserDashboard() {
    const [token,,,,,userInfo] = useToken()

    return(
        <>
        {userInfo &&
            <h1>Welcome back {userInfo.name}!</h1>
        }
        <div>
            <NavLink to="/home/reminders" className={({isActive}) => (isActive ? "active-now": "inactive")}>
                <div className="dashboard-tabs">Reminders</div>
            </NavLink>
            <NavLink to="/home/contacts" className={({isActive}) => (isActive ? "active-now": "inactive")}>
                <div className="dashboard-tabs">contacts</div>
            </NavLink>
            <NavLink to="/home/templates" className={({isActive}) => (isActive ? "active-now": "inactive")}>
                <div className="dashboard-tabs">templates</div>
            </NavLink>
        </div>
        <Outlet/>
        </>
    )
}

export default UserDashboard