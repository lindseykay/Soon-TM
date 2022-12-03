import { useState, useEffect } from 'react'
import { useToken } from '../hooks/useToken'

function ContactDashboard(){
    const [token,,,,,userInfo] = useToken()
    const [recipientName, setRecipientName] = useState("")
    const [recipientPhone, setRecipientPhone] = useState("")
    const [recipientEmail, setRecipientEmail] = useState("")
    const [note, setNote] = useState("")
    const [specialDays, setSpecialDays] = useState([])
    const [specialDayShow, setSpecialDayShow] = useState(0)

    async function createContact(){
        
    }
        

    return(
        <>
            <input required placeholder="Name"
                type="text"
                className="form-option"
                autoComplete='ofasdasdasdasdasdasdasdf'
                maxLength={50}
                value={recipientName}
                onChange={e=>setRecipientName(e.target.value)}/>
            <input placeholder="Phone"
                type="text"
                className="form-option"
                maxLength={20}
                autoComplete='ofasdasdasdasdasdasdasdf'
                value={recipientPhone}
                onChange={e=>setRecipientPhone(e.target.value)}/>
            <input placeholder="Email"
                type="text"
                className="form-option"
                maxLength={64}
                autoComplete='ofasdasdasdasdasdasdasdf'
                value={recipientEmail}
                onChange={e=>setRecipientEmail(e.target.value)}/>
            <textarea required placeholder="Notes"
                name="message"
                className="form-option"
                value={note}
                onChange={e=>setNote(e.target.value)}
                rows="5"></textarea>
        </>
    )
}

export default ContactDashboard