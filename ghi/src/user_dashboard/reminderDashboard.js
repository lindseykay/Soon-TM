import { useState, useEffect } from 'react'
import { useToken } from '../hooks/useToken'

async function getReminders(token) {
    const url = `${process.env.REACT_APP_REMINDERS_HOST}/reminders/`
    try {
        const response = await fetch(url, {
            method: 'get',
            headers: {
                "Authorization": `Bearer ${token}`
            }
        })
        if(response.ok) {
            const data = await response.json()
            return data
        }
    }
    catch(e){
        return []
    }
}

function ReminderDashboard(){
    const [token,,,,,userInfo] = useToken()
    const [reminderList, setReminderList] = useState([])
    const [filteredReminders, setFilteredReminders] = useState([])

    useEffect(() => {
        const newReminders = async() =>{
            const reminders = await getReminders(token)
            setReminderList(reminders)
            filterReminders(0, reminders)
        }
        if (token){
            newReminders()
        }
    }, [token])

    function filterReminders(val, rlist = reminderList){
        let today = new Date()
        today = today.toISOString().split('T')[0]

        if (val === 0 ){
            const list = rlist.filter(obj => obj.reminder_date === today)
            setFilteredReminders(list)
        }
        if (val === 1 ){
            const list = rlist.filter(obj => obj.reminder_date > today)
            setFilteredReminders(list)
        }
        if (val === 2 ){
            const list = rlist.filter(obj => obj.reminder_date < today)
            setFilteredReminders(list)
        }
    }

    return(
        <>
        <h1>Hi this is reminder Dashboard</h1>
        <button onClick={e => filterReminders(0)}>Today's reminders</button>
        <button onClick={e => filterReminders(1)}>Scheduled Reminders</button>
        <button onClick={e => filterReminders(2)}>Past Reminders</button>
        {
            filteredReminders.map(reminder => {
                return(
                    <li key = {reminder.id}>{reminder.message.content}{reminder.reminder_date}</li>
                )
            })
        }
        </>
    )
}

export default ReminderDashboard