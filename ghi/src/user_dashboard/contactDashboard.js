import { useState, useEffect } from "react";
import { useToken } from "../hooks/useToken";
import { getContacts } from "../dataLoadFunctions";
import ContactBook from "../contacts/contactsBook";

function ContactDashboard() {
  const [token] = useToken();
  const [contactsList, setContactsList] = useState([]);
  const [counter, setCounter] = useState(0);

  useEffect(() => {
    if (token) {
      const newContacts = async () => {
        const contacts = await getContacts(token);
        setContactsList(contacts);
      };
      newContacts();
    }
  }, [token, counter]);

  return (
    <div className="subdisplay-container">
      <ContactBook
        contacts={contactsList}
        setCounter={setCounter}
        counter={counter}
      />
    </div>
  );
}

export default ContactDashboard;
