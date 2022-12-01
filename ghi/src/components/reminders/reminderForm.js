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
            setRecipientFormShow(0)
        } else {
            alert("Please provide a name!")
        }
    }

    const removeRecipient = (e,idx) => {
        e.stopPropagation()
        const newList = [...recipientList]
        newList.splice(idx,1)
        setRecipientList(newList)
    }

    function formSubmission(event) {
        event.preventDefault()
        setEmailTarget("")
        setRecipientList([])
        setReminderDate("")
        setMessage("")
    }

    function tomorrow() {
        let nextDay = new Date();
        nextDay.setDate(nextDay.getDate() + 1);

        let month = nextDay.getMonth() + 1;
        let day = nextDay.getDate();
        let year = nextDay.getFullYear();

        if (month < 10) { month = "0" + month }
        if (day < 10) { day = "0" + day }

        return year + '-' + month + '-' + day;
    }

    return (
        <>
            <div className="outer-container"></div>
            <div className="reminder-form-container">
                <form>
                    {anonFlag &&
                    <div className="form-input">
                        <label htmlFor="target-email">Your email:</label><br/>
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
                            <label htmlFor="recipients">To whom:</label><br/>
                            <div placeholder= "Click to add recipients"
                                name="recipients"
                                className="form-option"
                                onClick={e=>setRecipientFormShow(1)}>
                                {recipientList.map((recipient, idx) => {
                                    return (
                                        <div className='recipient'
                                            key={recipient.name+idx}>
                                            {recipient.name}
                                            <div className='delete-mark'
                                                onClick={e=>removeRecipient(e,idx)}>
                                                <div className='x-mark'>x</div>
                                            </div>
                                        </div>
                                    )
                                })}
                            </div>
                        </>
                        }
                        {recipientFormShow === 1 &&
                        <>
                            <label>To whom:</label><br/>
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
                            <button className="form-return-button" onClick={e=>setRecipientFormShow(0)}>Return</button>
                        </>
                        }
                    </div>
                    <div className="form-input">
                        <label htmlFor="reminder-date">Remind me on:</label><br/>
                        <input required placeholder="When do you want to receive this?"
                            type="date"
                            name="reminder-date"
                            min={tomorrow()}
                            className="form-option"
                            value={reminderDate}
                            onChange={e=>setReminderDate(e.target.value)}/>
                    </div>
                    <div className="form-input">
                        <label htmlFor="message">Message:</label><br/>
                        <textarea required placeholder="Your reminder message"
                            name="message"
                            className="form-option"
                            value={message}
                            onChange={e=>setMessage(e.target.value)}
                            rows="5"></textarea>
                    </div>
                    <button onClick={e=>formSubmission(e)}>Submit reminder</button>
                </form>
            </div>
        </>
    )
}

export default ReminderForm;
