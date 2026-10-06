import { useState, useEffect } from 'react';
import './Register.css'

function Register() {

    const [showPassword, setShowPassword] = useState(false)
    const [showConfirmPassword, setShowConfirmPassword] = useState(false)

    const [username, setUsername] = useState("")

    const [usernameAvailability, setUsernameAvailability] = useState(null)

    const [focusedField, setFocusedField] = useState<
        "username" | "email" | null
    >(null);

    useEffect(() => {

        const timer = setTimeout(async () => {

            if (username.length < 5){
                setUsernameAvailability(null);
                return;
            }

            const response = await fetch(
                `http://localhost:8000/check-username?username=${username}`
            );

            const data = await response.json();

            setUsernameAvailability(data.available)

        }, 400);

        return () => {
            clearTimeout(timer)
        };
    }, [username]);

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
                        onFocus={() => setFocusedField("username")}
                        minLength={5}
                        maxLength={20}
                        spellCheck={false}
                        autoComplete='username'
                    />

                    {focusedField === "username" && 
                        username.length >= 5 && 
                        usernameAvailability === true &&(
                        <p className='username-available'>
                            ✓ Username available
                        </p>
                    )}

                    {focusedField === "username" && 
                        username.length >= 5 && 
                        usernameAvailability === false &&(
                        <p className='username-taken'>
                            ✕ Username already taken
                        </p>
                    )}

                    {username.length > 0 && username.length < 5 && (
                        <p className='username-error'>
                            Username must be at least 5 characters.
                        </p>
                    )}
                </div>

                <div>
                    <label htmlFor="email">Email</label>
                    <input 
                        id='email' 
                        type="email" 
                        placeholder='you@example.com'
                        onFocus={() => setFocusedField("email")}
                    />
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