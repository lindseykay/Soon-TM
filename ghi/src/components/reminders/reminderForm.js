import { useState } from 'react'

function ReminderForm() {
    const [anonFlag, setAnonFlag] = useState(true)
    const [emailTarget, setEmailTarget] = useState("")
    const [recipientName, setRecipientName] = useState("")
    const [recipientPhone, setRecipientPhone] = useState("")
    const [recipientEmail, setRecipientEmail] = useState("")
    const [reminderDate, setReminderDate] = useState("")
    const [message, setMessage] = useState("")
    const [recipientFormShow, setRecipientFormShow] = useState(0)
    const [recipientList, setRecipientList] = useState([])
    const [recipientListNames, setRecipientListNames] = useState("")

    const submitRecipient = () => {
        let recipient = {
            name: recipientName,
            phone: recipientPhone,
            email: recipientEmail
        }
        if (recipient.name.length > 0) {
            let rlist = recipientList
            rlist.push(recipient)
            setRecipientList(rlist)
            setRecipientName("")
            setRecipientPhone("")
            setRecipientEmail("")
            updateRecipientNames(rlist)
            setRecipientFormShow(0)
        } else {
            alert("Please provide a name!")
        }
    }

    function updateRecipientNames(rlist) {
        let rnames = rlist.reduce((a,b) => a.concat(', ',b.name), "")
        rnames = rnames.substring(2, rnames.length)
        setRecipientListNames(rnames)
    }

    const removeRecipient = (idx) => {
        const newList = [...recipientList]
        newList.splice(idx,1)
        setRecipientList(newList)
        updateRecipientNames(newList)
    }

    return (
        <div className="reminder-form-container">
            <form>
                {anonFlag &&
                <div className="form-input">
                    <label htmlFor="target-email">Your email:</label>
                    <input required placeholder="Your own email address"
                        type="text"
                        name="target-email"
                        className="form-option"
                        value={emailTarget}
                        onChange={e=>setEmailTarget(e.target.value)}/>
                </div>}
                <div className="form-input">
                    {recipientFormShow === 0 &&
                    <>
                        <label htmlFor="recipients">To whom:</label>
                        <input required placeholder="Who do you want to reach out to?"
                            type="text"
                            name="recipients"
                            className="form-option"
                            value={recipientListNames || ""}
                            readOnly
                            onClick={e=>setRecipientFormShow(1)}/>
                        <button onClick={e=>setRecipientFormShow(2)}>Edit recipients</button>
                    </>
                    }
                    {recipientFormShow === 1 &&
                    <>
                        <input required placeholder="Name"
                            type="text"
                            className="form-option"
                            autoComplete='ofasdasdasdasdasdasdasdf'
                            value={recipientName}
                            onChange={e=>setRecipientName(e.target.value)}/>
                        <input placeholder="Phone"
                            type="text"
                            className="form-option"
                            autoComplete='ofasdasdasdasdasdasdasdf'
                            value={recipientPhone}
                            onChange={e=>setRecipientPhone(e.target.value)}/>
                        <input placeholder="Email"
                            type="text"
                            className="form-option"
                            autoComplete='ofasdasdasdasdasdasdasdf'
                            value={recipientEmail}
                            onChange={e=>setRecipientEmail(e.target.value)}/>
                        <br/>
                        <button onClick={submitRecipient}>Add recipient</button>
                        {!anonFlag &&
                        <button>Add from contacts</button>}
                        <button onClick={e=>setRecipientFormShow(0)}>Return</button>
                    </>
                    }
                    {recipientFormShow === 2 &&
                    <>
                        {recipientList.map((recipient, idx) => {
                            return(
                                <div key={recipient.name.concat(String(idx))}>
                                    <p>Name: {recipient.name}</p>
                                    <p>Phone: {recipient.phone}</p>
                                    <p>Email: {recipient.email}</p>
                                    <button onClick={e=>removeRecipient(idx)}>Remove</button>
                                </div>
                            )
                        })
                        }
                        <button onClick={e=>setRecipientFormShow(0)}>Return</button>
                    </>
                    }
                </div>
                <div className="form-input">
                    <label htmlFor="reminder-date">Remind me on:</label>
                    <input required placeholder="When do you want to receive this?"
                        type="date"
                        name="reminder-date"
                        className="form-option"
                        value={reminderDate}
                        onChange={e=>setReminderDate(e.target.value)}/>
                </div>
                <div className="form-input">
                    <label htmlFor="message">Message</label>
                    <textarea required placeholder="Your reminder message"
                        name="message"
                        className="form-option"
                        value={message}
                        onChange={e=>setMessage(e.target.value)}
                        rows="4"></textarea>
                </div>
            </form>
        </div>
    )
}

export default ReminderForm;
