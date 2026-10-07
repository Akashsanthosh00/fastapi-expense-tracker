import { useState, useEffect } from 'react';
import './Register.css'
import { Eye, EyeOff } from "lucide-react";

function Register() {

    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const [username, setUsername] = useState("");

    const [usernameAvailability, setUsernameAvailability] = useState(null);

    const [focusedField, setFocusedField] = useState<
        "username" | "email" |"password" | "confirmPassword" | null
    >(null);

    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    const passwordRules = {
        length: password.length >= 8 && password.length <= 16,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[^A-Za-z0-9]/.test(password),
    }

    const [confirmPassword, setConfirmPassword] = useState("");

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
                        value = {email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder='you@example.com'
                        onFocus={() => setFocusedField("email")}
                    />
                </div>

                <div>
                    <label htmlFor="password">Password</label>

                    <div className='password-input-wrapper'>
                        <input 
                            id="password"
                            value = {password}
                            onChange={(e) => setPassword(e.target.value)}
                            type={showPassword ? "text": "password"}
                            placeholder='Min. 8 characters'
                            minLength={8}
                            maxLength={16}
                            onFocus={() => setFocusedField("password")}
                        />

                        <button
                            type='button'
                            className='password-toggle'
                            onClick={ () => setShowPassword(!showPassword)}
                            aria-label={showPassword ? "Hide password": "Show password"}
                        >
                            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                        </button>

                    </div>

                    {focusedField === "password" && (
                        <div className='password-rules'>
                            <p>Password must contain:</p>

                            <div className={passwordRules.length ? "rule-valid" : "rule-invalid"}>
                                {passwordRules.length ? "✓" : "✕"} 8-16 characters
                            </div>

                            <div className={passwordRules.uppercase ? "rule-valid" : "rule-invalid"}>
                                {passwordRules.uppercase ? "✓" : "✕"} one uppercase letter
                            </div>

                            <div className={passwordRules.lowercase ? "rule-valid" : "rule-invalid"}>
                                {passwordRules.lowercase ? "✓" : "✕"} one lowercase letter
                            </div>

                            <div className={passwordRules.number ? "rule-valid" : "rule-invalid"}>
                                {passwordRules.number ? "✓" : "✕"} one number
                            </div>

                            <div className={passwordRules.special ? "rule-valid" : "rule-invalid"}>
                                {passwordRules.special ? "✓" : "✕"} one special character
                            </div>

                        </div>
                    )}

                </div>

                <div>
                    <label htmlFor="confirm-password">Confirm Password</label>

                    <div className='password-input-wrapper'>
                        <input 
                            id="confirm-password" 
                            type={showConfirmPassword ? "text": "password"}
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder='Re-enter your password'
                            onFocus={() => setFocusedField("confirmPassword")}
                        />

                        <button 
                            type='button'
                            className='password-toggle'
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                            aria-label={showConfirmPassword ? "Hide": "Show"}
                            >
                                {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                        </button>

                    </div>

                    {focusedField === "confirmPassword" && confirmPassword.length > 0 && (
                        <p className={
                            password === confirmPassword
                                ? "password-match"
                                : "password-mismatch"
                        }>
                            {password === confirmPassword
                                ? "✓ Passwords match"
                                : "✕ Passwords do not match"
                            }
                        </p>
                    )}
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