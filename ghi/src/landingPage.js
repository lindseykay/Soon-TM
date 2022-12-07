import { Link } from "react-router-dom";

function LandingPage() {
  return (
    <>
      <div className="landing-page-welcome">
        let's make "soon" happen
        <div className="create-reminder-button">
          <Link to="/reminders/new">
            <button>create a reminder</button>
          </Link>
        </div>
        <div className="phone">
          <img src={require("./assets/phone-landing-page.png")} alt="phone.png" />
        </div>
      </div>
    </>
  );
}

export default LandingPage;
