import { useState, useEffect } from 'react'
import CreateContact from '../contacts/createContact'
import { useToken } from '../hooks/useToken'

function ContactDashboard(){
    const [token,,,,,userInfo] = useToken()
    
    return(
        <>
        <CreateContact/>
        </>
    )
}

export default ContactDashboard