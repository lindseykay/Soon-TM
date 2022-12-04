import { useState, useEffect } from 'react'
import { useToken } from '../hooks/useToken'
import getReminders from '../dataLoadFunctions'

function ReminderDashboard(props){
    const [token] = useToken()
    const [filteredReminders, setFilteredReminders] = useState([])

    const newReminders = async () => {
            const reminders = await getReminders(token)
            props.refreshReminders(reminders)
            filterReminders(0, reminders)
        }

    useEffect(() => {
        if (token && !props.reminderList){
            newReminders()
        }
    }, [token])

    function filterReminders(val, rlist = props.reminderList){
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
