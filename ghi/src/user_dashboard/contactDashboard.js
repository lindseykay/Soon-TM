import { useState, useEffect } from 'react'
import CreateContact from '../contacts/createContact'
import { useToken } from '../hooks/useToken'
import { getContacts } from '../dataLoadFunctions'
import { Link } from 'react-router-dom'

function ContactDashboard(){
    const [token,,,,,userInfo] = useToken()
    const [contactsList, setContactsList] = useState([])
    const [counter, setCounter] = useState(0)
    const [showCreationForm, setShowCreationForm] = useState(false)

    const newContacts = async () => {
        const contacts = await getContacts(token)
        setContactsList(contacts)
    }

    useEffect(() => {
        if (token) {
            newContacts()
        }
    }, [token, counter])

    return(
        <>
            {!showCreationForm &&
            <button onClick={e=>setShowCreationForm(true)}>Add new contact</button>
            }
            {!showCreationForm &&
            contactsList.map(contact => {
                return (
                    <div key={contact.id}>
                        <div>{contact.recipient.name}</div>
                        <Link to="/reminders/new" state={{
                            recName: contact.recipient.name,
                            recPhone: contact.recipient.phone,
                            recEmail: contact.recipient.email,
                            recID: contact.id
                        }}>Send Reminder</Link>
                    </div>
                )
            })
            }
            {showCreationForm &&
                <CreateContact
                    refreshContacts={setCounter}
                    counter={counter}
                    showForm={setShowCreationForm}/>
            }
        </>
    )
}

export default ContactDashboard
