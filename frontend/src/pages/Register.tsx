import './Register.css'

function Register() {
  return (
    <div className="register-page">
        
        <div className='brand'>
            <span className='logo-icon'>ET</span>
            <span>Expense Tracker</span>
        </div>

        <h2>Create your account</h2>
        <p>Start tracking your expenses in minutes</p>

        <div className="login-container">

            <form>
                <div>
                    <label htmlFor='username'>Username</label>
                    <input id="username" type="text" placeholder='e.g. akash_s'/>
                </div>

                <div>
                    <label htmlFor="email">Email</label>
                    <input id='email' type="email" placeholder='you@example.com'/>
                </div>

                <div>
                    <label htmlFor="password">Password</label>
                    <input id="password" type="password" placeholder='Min. 12 characters'/>
                </div>

                <div>
                    <label htmlFor="confirm-password">Confirm Password</label>
                    <input id="confirm-password" type="password" placeholder='Re-enter your password' />
                </div>

                <button className='submit-button'>Create account</button>
            </form>

        </div>

        <div className='register-link'>
            <span>Already have an account?</span> <a href="#">Sign in</a>
        </div>
    </div>
  );
}

export default Register;