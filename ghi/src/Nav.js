import { useToken } from "./hooks/useToken";
import LoginWidget from "./loginWidget";

function NavBar() {
    const [token,,logout] = useToken()

    return (
        <div className="nav-bar">
            {!token &&
                <LoginWidget />
            }
            {token &&
                <>
                    <div>menu placeholder</div>
                    <button onClick={e=>logout()}>Log out</button>
                </>
            }
        </div>
    )
}

export default NavBar
