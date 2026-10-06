import { useState, useEffect } from 'react';
import './Register.css'

function Register() {

    const [showPassword, setShowPassword] = useState(false)
    const [showConfirmPassword, setShowConfirmPassword] = useState(false)

    const [username, setUsername] = useState("")

    useEffect(() => {

        if (username.length < 5){
            return
        }

        const timer = setTimeout(() => {
            console.log("Checking username...")
        }, 400)

        return () => {
            clearTimeout(timer)
        }
    }, [username])

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

                    <input
                        id="username" 
                        type="text" 
                        placeholder='e.g. akash_s'
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        minLength={5}
                        maxLength={20}
                    />

                    {username.length > 0 && username.length < 5 && (
                        <p className='username-error'>
                            Username must be at least 5 characters.
                        </p>
                    )}
                </div>

                <div>
                    <label htmlFor="email">Email</label>
                    <input id='email' type="email" placeholder='you@example.com'/>
                </div>

                <div>
                    <label htmlFor="password">Password</label>
                    <input 
                        id="password" 
                        type={showPassword ? "text": "password"}
                        placeholder='Min. 12 characters'
                    />

                    <button 
                        type='button' onClick={() => 
                        setShowPassword(!showPassword)}
                        >
                        {showPassword ? "Hide": "Show"}
                    </button>

                </div>

                <div>
                    <label htmlFor="confirm-password">Confirm Password</label>
                    <input 
                        id="confirm-password" 
                        type={showConfirmPassword ? "text": "password"} 
                        placeholder='Re-enter your password' 
                    />

                    <button 
                        type='button' onClick={() => 
                        setShowConfirmPassword(!showConfirmPassword)}
                        >
                            {showConfirmPassword ? "Hide": "Show"}
                    </button>
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