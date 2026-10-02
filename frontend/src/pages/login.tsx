import './Login.css'

function Login() {
  return (
    <div className="login-page">
        <h2>Login</h2>
        
        <form>
            <div>
                <label>Username: </label>
                <input type="text"/>
            </div>

            <div>
                <label>Password: </label>
                <input type="password"/>
            </div>

            <button>Login</button>
        </form>
    </div>
  );
}

export default Login;