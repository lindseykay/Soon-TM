import { useState, useEffect } from "react";
import { useToken } from "../hooks/useToken";
import { getContacts } from "../dataLoadFunctions";
import ContactBook from "../contacts/contactsBook";

function ContactDashboard() {
  const [token] = useToken();
  const [contactsList, setContactsList] = useState([]);
  const [counter, setCounter] = useState(0);

  const newContacts = async () => {
    const contacts = await getContacts(token);
    setContactsList(contacts);
  };

  useEffect(() => {
    if (token) {
      newContacts();
    }
  }, [token, counter]);

  return (
    <>
      <ContactBook
        contacts={contactsList}
        setCounter={setCounter}
        counter={counter}
      />
    </>
  );
}

export default ContactDashboard;
