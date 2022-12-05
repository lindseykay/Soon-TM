async function getReminders(token) {
  const url = `${process.env.REACT_APP_REMINDERS_HOST}/reminders/`;
  try {
    const response = await fetch(url, {
      method: "get",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.ok) {
      const data = await response.json();
      console.log("RONRONRONRONRON:", data);
      return data;
    }
  } catch (e) {
    return [];
  }
}

export async function getContacts(token) {
  const url = `${process.env.REACT_APP_CONTACTS_HOST}/contacts/`;
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

export default getReminders;
