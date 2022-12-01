import { BrowserRouter, Routes, Route} from 'react-router-dom';
import ReminderForm from './components/reminders/reminderForm';

function App() {

  return (
    <BrowserRouter>
      <main>
        <Routes>
          <Route path="/" element={<></>}/>
          <Route path="home" element={<></>}/>
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
            <Route index element={<></>}/>
            <Route path="new" element={<></>}/>
            <Route path=":id" element={<></>}/>
          </Route>
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App;
