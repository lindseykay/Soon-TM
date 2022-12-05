async function deleteReminder(reminderId, token) {
  const url = `${process.env.REACT_APP_REMINDERS_HOST}/reminder/${reminderId}`;
  try {
    const response = await fetch(url, {
      method: "DELETE",
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

export default deleteReminder;
