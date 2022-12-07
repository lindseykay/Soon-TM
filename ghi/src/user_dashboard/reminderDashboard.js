import { useState, useEffect } from "react";
import { useToken } from "../hooks/useToken";
import getReminders from "../dataLoadFunctions";
import deleteReminder from "../deleteReminder";

function ReminderDashboard(props) {
  const [token] = useToken();
  const [filteredReminders, setFilteredReminders] = useState([]);
  const [counter, setCounter] = useState(0);

  const newReminders = async () => {
    const reminders = await getReminders(token);
    props.refreshReminders(reminders);
    filterReminders(0, reminders);
  };

  useEffect(() => {
    if (token && !props.reminderList) {
      newReminders();
    } else if (props.reminderList) {
      filterReminders(0);
    }
  }, [token]);

  useEffect(() => {
    if (token) {
      newReminders();
    }
  }, [counter]);

  function filterReminders(val, rlist = props.reminderList) {
    let today = new Date();
    today = today.toISOString().split("T")[0];

    const buttons = document.querySelectorAll(".reminder-tabs");
    for (let node of buttons) {
      node.classList.remove("selected-tab");
    }

    const button = document.querySelector(`#reminder-tab-${val}`);
    if (val === 0) {
      const list = rlist.filter((obj) => obj.reminder_date === today);
      setFilteredReminders(list);
      button.classList.add("selected-tab");
    }
    if (val === 1) {
      const list = rlist.filter((obj) => obj.reminder_date > today);
      setFilteredReminders(list);
      button.classList.add("selected-tab");
    }
    if (val === 2) {
      const list = rlist.filter((obj) => obj.reminder_date < today);
      setFilteredReminders(list);
      button.classList.add("selected-tab");
    }
  }

  return (
    <>
      <button
        className="reminder-tabs"
        id="reminder-tab-0"
        onClick={(e) => filterReminders(0)}
      >
        Today's reminders
      </button>
      <button
        className="reminder-tabs"
        id="reminder-tab-1"
        onClick={(e) => filterReminders(1)}
      >
        Scheduled Reminders
      </button>
      <button
        className="reminder-tabs"
        id="reminder-tab-2"
        onClick={(e) => filterReminders(2)}
      >
        Past Reminders
      </button>
      <div className="reminder-list-box">
        {filteredReminders.map((reminder) => {
          return (
            <div className="reminder" key={reminder.id}>
              <div className="heading">
                Message for: &nbsp;
                {reminder.recipients
                  .reduce((a, b) => a + `, ${b.name}`, "")
                  .substring(2)
                  .toUpperCase()}
              </div>
              <div className="content"> {reminder.message.content}</div>
              <div className="footer">
                Sending on: {reminder.reminder_date}
                <span className="update-options">
                  <span>edit</span> |{" "}
                  <span
                    className="delete-tab"
                    id="delete-tab"
                    onClick={(e) => {
                      deleteReminder(reminder.id, token);
                      setCounter(counter + 1);
                    }}
                  >
                    delete
                  </span>
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </>
  );
}

export default ReminderDashboard;
