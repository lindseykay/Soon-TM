import { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, useNavigate, Outlet } from 'react-router-dom';
import ReminderForm from './reminders/reminderForm';
import LandingPage from './landingPage';
import ContactBook from './contacts/contactsBook';
import { AuthProvider, useToken } from './hooks/useToken';
import NavBar from './Nav';
import UserDashboard from './user_dashboard/userDashboard';
import ReminderDashboard from './user_dashboard/reminderDashboard';
import ContactDashboard from './user_dashboard/contactDashboard';
import TemplateDashboard from './user_dashboard/templateDashboard';


function GetToken() {
    // Get token from JWT cookie (if already logged in)
    useToken();
    return null
}

//Route protection
function AuthRoute ({children}) {
    const [token] = useToken()
    const [counter, setCounter] = useState(0)
    const navigate = useNavigate()

    useEffect(()=>{
      if (!token && counter < 1) {
        setCounter(counter+1)
      } else if (!token && counter >= 1) {
        navigate('/')
      }
    },[token])

    if (token) {
      return children ? children : <Outlet />
    }
}

function App() {
  const [reminderList, setReminderList] = useState()

  return (
    <AuthProvider>
      <BrowserRouter>
        <GetToken/>
        <NavBar/>
        <div className="main-display">
          <Routes>
            <Route path="/" element={<LandingPage/>}/>
            <Route path="home" element={
              <AuthRoute>
                <UserDashboard/>
              </AuthRoute>
              }>
              <Route path="reminders" element={<ReminderDashboard reminderList={reminderList} refreshReminders={setReminderList}/>}/>
              <Route path="contacts" element={<ContactDashboard/>}/>
              <Route path="templates" element={<TemplateDashboard/>}/>
            </Route>
            <Route path="reminders">
              <Route path="new" element={<ReminderForm refreshReminders={setReminderList}/>}/>
              <Route path=":id" element={<></>}/>
            </Route>
            <Route path="templates">
              <Route index element={<></>}/>
              <Route path="new" element={<></>}/>
              <Route path=":id" element={<></>}/>
            </Route>
            <Route path="contacts">
              <Route index element={<></>}/>
              <Route path="new" element={<></>}/>
              <Route path=":id" element={<></>}/>
            </Route>
          </Routes>
        </div>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App;
