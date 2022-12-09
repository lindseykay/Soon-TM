import { useState, useEffect } from "react";
import { useToken } from "../hooks/useToken";
import { getContacts } from "../dataLoadFunctions";
import ContactBook from "../contacts/contactsBook";

function ContactDashboard(props) {
  const [token] = useToken();
  const [emptyFlag, setEmptyFlag] = useState(false);

  useEffect(() => {
    if (token && props.contactsList.length === 0 && !emptyFlag) {
      const newContacts = async () => {
        const contacts = await getContacts(token);
        props.updateContacts(contacts);
        if (contacts.length === 0) {
          setEmptyFlag(true);
        }
      };
      newContacts();
    } else if (props.contactsList.length > 0 && emptyFlag) {
      setEmptyFlag(false);
    }
  }, [props.contactsList]); // eslint-disable-line

  return (
    <div className="subdisplay-container">
      <ContactBook
        contactsList={props.contactsList}
        updateContacts={props.updateContacts}
      />
    </div>
  );
}

export default ContactDashboard;
