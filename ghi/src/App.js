import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import ReminderForm from './reminders/reminderForm';
import LandingPage from './landingPage';
import ContactBook from './contacts/contactsBook';
import { AuthProvider, useToken } from './hooks/useToken';

import NavBar from './Nav';
import UserDashboard from './user_dashboard/userDashboard';
import ReminderDashboard from './user_dashboard/reminderDashboard';
import ContactDashboard from './user_dashboard/contactDashboard';
import TemplateDashboard from './user_dashboard/templateDashboard';
import SettingsDashboard from './user_dashboard/settingsDashboard';


function GetToken() {
    // Get token from JWT cookie (if already logged in)
    useToken();
    return null
}

function App() {

  return (
    <AuthProvider>
      <BrowserRouter>
        <GetToken/>
        <NavBar/>
        <main>
          <Routes>
            <Route path="/" element={<LandingPage/>}/>
            <Route path="home" element={<UserDashboard/>}>
              <Route path="reminders" element={<ReminderDashboard/>}/>
              <Route path="contacts" element={<ContactDashboard/>}/>
              <Route path="templates" element={<TemplateDashboard/>}/>
              <Route path="settings" element={<SettingsDashboard/>} />
            </Route>
            <Route path="reminders">
              <Route path="new" element={<ReminderForm/>}/>
              <Route path=":id" element={<></>}/>
            </Route>
            <Route path="templates">
              <Route index element={<></>}/>
              <Route path="new" element={<></>}/>
              <Route path=":id" element={<></>}/>
            </Route>
            <Route path="contacts">
              {/* <Route index element={<ContactBook/>}/> */}
              <Route path="new" element={<></>}/>
              <Route path=":id" element={<></>}/>
            </Route>
          </Routes>
        </main>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App;
