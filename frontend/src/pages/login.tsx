import './Login.css'

function Login() {
  return (
    <div className="login-page">

        <div className='login-logo'>
            Logo
        </div>
        <h2>Sign in to Expense Tracker</h2>

        <div className="login-container">

            <form>
                <div>
                    <label htmlFor='username'>Username</label>
                    <input id="username" type="text"/>
                </div>

                <div className="password-field">
                    <div className="password-label">
                        <label htmlFor="password">Password</label>
                        <a href="#">Forgot password?</a>
                    </div>

                    <input id="password" type="password" />
                </div>

                <button>Sign in</button>
            </form>

        </div>

        <div className='register-link'>
            <span>New user?</span> <a href="#">Create an account</a>
        </div>
    </div>
  );
}

export default Login;