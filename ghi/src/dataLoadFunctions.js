async function getReminders(token) {
  const url = `${process.env.REACT_APP_REMINDERS_HOST}/reminders`;
  try {
    const response = await fetch(url, {
      method: "get",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.ok) {
      const data = await response.json();
      return data;
    }
  } catch (e) {
    return [];
  }
}

export async function getContacts(token) {
  const url = `${process.env.REACT_APP_CONTACTS_HOST}/contacts`;
  try {
    const response = await fetch(url, {
      method: "get",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.ok) {
      const data = await response.json();
      return data;
    }
  } catch (e) {
    return [];
  }
}

export async function deleteContact(contactId, token) {
  const url = `${process.env.REACT_APP_CONTACTS_HOST}/contacts/${contactId}`;
  try {
    const response = await fetch(url, {
      method: "delete",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.ok) {
      const data = await response.json();
      return data;
    }
  } catch (e) {
    return false;
  }
}

export default getReminders;
