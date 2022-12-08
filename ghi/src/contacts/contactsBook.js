import { useState } from "react";
import { Link } from "react-router-dom";
import { CreateContact } from "./createContact";
import { deleteContact } from "../dataLoadFunctions";
import { useToken } from "../hooks/useToken";
import "./contactBook.css";

function ContactBook(props) {
  const [token] = useToken();
  const [pageNum, setPageNum] = useState(1);
  const [showCreationForm, setShowCreationForm] = useState(false);

  const nextPageFlip = (event) => {
    const page = document.querySelector(`#page-${pageNum}`);
    if (
      page.nextElementSibling &&
      !page.nextElementSibling.hasAttribute("title")
    ) {
      page.classList.add("flipped");
      page.classList.remove("bordered-right");
      page.classList.add("bordered-left");
      page.nextElementSibling.classList.add("flipped");
      page.nextElementSibling.classList.remove("bordered-right");
      page.nextElementSibling.classList.add("bordered-left");
      setPageNum(pageNum + 2);
    }
  };

  const prevPageFlip = (event) => {
    let page = document.querySelector(`#page-${pageNum - 1}`);
    page.classList.remove("flipped");
    page.classList.remove("bordered-left");
    page.classList.add("bordered-right");
    page.previousElementSibling.classList.remove("flipped");
    page.previousElementSibling.classList.remove("bordered-left");
    page.previousElementSibling.classList.add("bordered-right");
    if (pageNum >= 3) {
      setPageNum(pageNum - 2);
    }
  };

  const sortedList = props.contacts
    .map((obj) => {
      return {
        contact_id: obj.id,
        recipient_id: obj.recipient.id,
        name: obj.recipient.name,
        phone: obj.recipient.phone,
        email: obj.recipient.email,
        notes: obj.notes,
        special_days: obj.special_days,
      };
    })
    .sort((a, b) =>
      a.name.toLowerCase() > b.name.toLowerCase()
        ? 1
        : b.name.toLowerCase() > a.name.toLowerCase()
        ? -1
        : 0
    );

  const listGroupsOfN = (list, n) => {
    const output = [];
    for (let p = 0; p < list.length; p += n) {
      if (p + n > list.length) {
        output.push(list.slice(p));
      } else {
        output.push(list.slice(p, p + n));
      }
    }
    return output;
  };

  return (
    <>
      <div className="book-cover">
        <div className="book">
          <div id="pages" className="pages">
            <div className="right-flip"></div>
            <div className="left-flip"></div>
            {sortedList.length === 0 && (
              <div className="page bordered-right">
                <div className="contact-instruction">
                  click add contacts below to get started
                </div>
              </div>
            )}
            {listGroupsOfN(sortedList, 3).map((groupOf3, idx) => {
              return (
                <div
                  className={`page bordered-${
                    (idx + 1) % 2 ? "right" : "left"
                  }`}
                  id={`page-${idx + 1}`}
                  key={`page-${idx + 1}`}
                  style={{ zIndex: (idx + 1) % 2 === 0 ? 10 : 99 - idx }}
                  onClick={(e) =>
                    (idx + 1) % 2 ? nextPageFlip(e) : prevPageFlip(e)
                  }
                >
                  <div className="contacts-container">
                    {groupOf3.map((contact, idx) => {
                      return (
                        <div className="contact" key={idx}>
                          <div className="contact-name">
                            {contact.name}
                            <Link
                              to="/soon-tm/reminders/new/"
                              state={{
                                recName: contact.name,
                                recPhone: contact.phone,
                                recEmail: contact.email,
                                recID: contact.recipient_id,
                              }}
                            >
                              <img
                                src={require("../assets/paper-plane.png")}
                                className="send-icon"
                                alt="send-icon"
                                title="send reminder"
                              />
                            </Link>
                            <img
                              src={require("../assets/trash.png")}
                              className="trash-icon"
                              alt="send-icon"
                              title="delete contact"
                              onClick={(e) => {
                                e.stopPropagation();
                                deleteContact(contact.contact_id, token);
                                props.setCounter(props.counter + 1);
                              }}
                            />
                          </div>
                          <div className="contact-phone">
                            <span>phone: </span>
                            {contact.phone}
                          </div>
                          <div className="contact-email">
                            <span>email: </span>
                            {contact.email}
                          </div>
                          <div className="contact-notes">
                            <span>notes: </span>
                            {contact.notes}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                  <div className="page-number">page {idx + 1}</div>
                </div>
              );
            })}
            {!showCreationForm && (
              <div
                className="show-contact-form"
                onClick={(e) => {
                  e.stopPropagation();
                  setShowCreationForm(true);
                }}
              >
                add contact
              </div>
            )}
          </div>
        </div>
      </div>
      {showCreationForm && (
        <CreateContact
          refreshContacts={props.setCounter}
          counter={props.counter}
          showForm={setShowCreationForm}
        />
      )}
    </>
  );
}

export default ContactBook;
