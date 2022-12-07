import { useEffect, useState } from "react";
import { useToken } from "../hooks/useToken";

function SettingsDashboard() {
  const [token, , , , update, userInfo] = useToken();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [nameModalOpen, setNameModalOpen] = useState(false);
  const [passwordModalOpen, setPasswordModalOpen] = useState(false);

  async function preventBlankPassword(event) {
    event.preventDefault();
    if (password.length === 0) {
      alert("Please provide an updated password");
    } else {
      update(password, userInfo.email, name);
    }
  }

  async function preventBlankName(event) {
    event.preventDefault();
    if (name.length === 0) {
      alert("Please provide an updated name");
    } else {
      update(password, userInfo.email, name);
    }
  }

  return (
    <>
      {userInfo && (
        <>
          <div>Username: {userInfo.username}</div>
          <div>
            name: {userInfo.name}
            <button
              className="update-button"
              onClick={(e) => setNameModalOpen(true)}
            >
              Update
            </button>
          </div>

          {nameModalOpen && (
            <div className="modal">
              <div className="modal-content">
                <button
                  className="close"
                  onClick={(e) => setNameModalOpen(false)}
                >
                  x
                </button>
                <div>
                  Upon submission, you will be automatically logged out and
                  redirected to the home page.
                </div>
                <input
                  placeholder={userInfo.name}
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
                <button
                  className="update-button"
                  onClick={(e) => preventBlankName(e)}
                >
                  Update Name
                </button>
              </div>
            </div>
          )}

          <div>
            Email: {userInfo.email}
            {/* <button className="update-button">Update</button> */}
          </div>

          <div>
            password: ********
            <button
              className="update-button"
              onClick={(e) => setPasswordModalOpen(true)}
            >
              Update
            </button>
          </div>

          {passwordModalOpen && (
            <div className="modal">
              <div className="modal-content">
                <div>
                  Upon submission, you will be automatically logged out and
                  redirected to the home page.
                </div>
                <button
                  className="close"
                  onClick={(e) => setPasswordModalOpen(false)}
                >
                  x
                </button>
                <input
                  type="text"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button
                  className="update-button"
                  onClick={(e) => preventBlankPassword(e)}
                >
                  Update Password
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </>
  );
}

export default SettingsDashboard;
