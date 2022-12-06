import { useState } from 'react'
import { useToken } from '../hooks/useToken'

export function CreateContact(props){
    const [token,,,,,userInfo] = useToken()
    const [recipientName, setRecipientName] = useState("")
    const [recipientPhone, setRecipientPhone] = useState("")
    const [recipientEmail, setRecipientEmail] = useState("")
    const [note, setNote] = useState("")
    const [specialDays, setSpecialDays] = useState([])
    const [specialDayShow, setSpecialDayShow] = useState(0)
    const [specialDayName, setSpecialDayName] = useState("")
    const [specialDayDate, setSpecialDayDate] = useState("")

    async function createContact(event){
        event.preventDefault()
        const recipient_id = await createRecipient()
        if (!recipient_id){
            alert("Recipient creation failed :(")
            return
        }
        const url = `${process.env.REACT_APP_CONTACTS_HOST}/contacts/`
        const body = JSON.stringify({
            contact: {
            "recipient_id": recipient_id,
            "notes": note
            },
            special_days: specialDays
        })
        const response = await fetch(url, {
            method: 'post',
            body: body,
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        })
        if (response.ok){
            props.refreshContacts(props.counter+1)
            setRecipientName("")
            setRecipientPhone("")
            setRecipientEmail("")
            setNote("")
            setSpecialDays([])
            props.showForm(false)
        }
    }

    async function createRecipient(){
        const url = `${process.env.REACT_APP_REMINDERS_HOST}/recipients/`
        const body = JSON.stringify({
            "name": recipientName,
            "phone": recipientPhone,
            "email": recipientEmail,
            "user_id": userInfo.id
        })
        const response = await fetch(url, {
            method: 'post',
            body: body,
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        })
        if (response.ok) {
            const data = await response.json()
            return data
        }
        return false
    }

    const submitSpecialDay= () => {
        let specialDay = {
            contact_id: 0,
            name: specialDayName,
            date: specialDayDate
        }
        if (specialDay.name && specialDay.date) {
            let sdays = specialDays
            sdays.push(specialDay)
            setSpecialDays(sdays)
            setSpecialDayName("")
            setSpecialDayDate("")
            setSpecialDayShow(0)
        } else {
            alert("Please fill out name & date")
        }
    }

    function removeSpecialDay(e,idx) {
        e.stopPropagation()
        const newList = [...specialDays]
        newList.splice(idx,1)
        setSpecialDays(newList)
    }

    return(
        <>
            <div className='dim-background' onClick={e=>props.showForm(false)}></div>
            <div className='contact-form-container'>
                <form>
                    <label>Add contact</label><br/>
                    <div className="form-input">
                        <input required placeholder="Name"
                            type="text"
                            className="form-option"
                            autoComplete='ofasdasdasdasdasdasdasdf'
                            maxLength={50}
                            value={recipientName}
                            onChange={e=>setRecipientName(e.target.value)}/>
                    </div>
                    <div className="form-input">
                        <input placeholder="Phone"
                            type="text"
                            className="form-option"
                            maxLength={20}
                            autoComplete='ofasdasdasdasdasdasdasdf'
                            value={recipientPhone}
                            onChange={e=>setRecipientPhone(e.target.value)}/>
                    </div>
                    <div className="form-input">
                        <input placeholder="Email"
                            type="text"
                            className="form-option"
                            maxLength={64}
                            autoComplete='ofasdasdasdasdasdasdasdf'
                            value={recipientEmail}
                            onChange={e=>setRecipientEmail(e.target.value)}/>
                    </div>
                    <div className="form-input">
                        {specialDayShow === 0 &&
                        <>
                            <div className="form-option"
                            onClick={e=>setSpecialDayShow(1)}>
                            {specialDays.map((specialday, idx) => {
                                return (
                                    <div className='contact'
                                        key={specialday.name+idx}>
                                        {specialday.name}
                                        <div className='delete-mark'
                                            onClick={e=>removeSpecialDay(e,idx)}>
                                            <div className='x-mark'>x</div>
                                        </div>
                                    </div>
                                )
                            })}
                            {specialDays.length === 0 &&
                            "Click here to add special days"
                            }
                            </div>
                        </>
                        }
                        {specialDayShow === 1 &&
                        <>
                            <input placeholder="Name"
                                type="text"
                                className="form-option"
                                autoComplete='ofasdasdasdasdasdasdasdf'
                                value={specialDayName}
                                onChange={e=>setSpecialDayName(e.target.value)}/>
                            <input placeholder="Date"
                                type="date"
                                className="form-option"
                                autoComplete='ofasdasdasdasdasdasdasdf'
                                value={specialDayDate}
                                onChange={e=>setSpecialDayDate(e.target.value)}/>
                            <button onClick={e=>submitSpecialDay()}>Add special day</button>
                            <button className="form-return-button" onClick={e=>setSpecialDayShow(0)}>return</button>
                        </>
                        }
                    </div>
                    <div className="form-input">
                        <textarea placeholder="Notes"
                            name="message"
                            className="form-option"
                            value={note}
                            onChange={e=>setNote(e.target.value)}
                            rows="5"></textarea>
                    </div>
                    <button onClick={e=>createContact(e)}>Submit</button>
                    <button onClick={e=>props.showForm(false)}>Return</button>
                </form>
            </div>
        </>
    )
}

export default CreateContact
