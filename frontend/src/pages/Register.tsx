import { useState, useEffect } from 'react';
import './Register.css'
import { Eye, EyeOff } from "lucide-react";

type UsernameStatus = "idle" | "checking" | "available" | "taken" | "error";

const USERNAME_PATTERN = /^[a-zA-Z0-9_]{5,20}$/;

const API_BASE_URL = import.meta.env.VITE_API_URL?.trim().replace(/\/+$/, "") ?? "";

function Register() {

    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const [username, setUsername] = useState("");

    const [touched, setTouched] = useState({
        username: false,
        email: false,
        password: false,
        confirmPassword: false,
    });

    const [usernameStatus, setUsernameStatus] = useState<UsernameStatus>("idle");

    const [focusedField, setFocusedField] = useState<"password" | null>(null);

    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    const [submitError, setSubmitError] = useState("")
    
    const [usernameCheckAttempt, setUsernameCheckAttempt] = useState(0);

    const passwordRules = {
        length: password.length >= 8 && password.length <= 64,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[^A-Za-z0-9\s]/.test(password),
        noSpaces: !/\s/.test(password)
    }

    const [confirmPassword, setConfirmPassword] = useState("");
    const usernameIsValid = USERNAME_PATTERN.test(username);

    const normalizedEmail = email.trim().toLowerCase();

    const emailIsValid =
                        normalizedEmail.length <= 254 &&
                        /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(normalizedEmail);

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        setTouched({
            username: true,
            email: true,
            password: true,
            confirmPassword: true,
        });

        setSubmitError("");

        if (!usernameIsValid){
            setSubmitError("Please enter a valid username.");
            return;
        }

        if (usernameStatus === "checking"){
            setSubmitError("Please wait while we check your username.");
            return;
        }

        if (usernameStatus === "error"){
            setSubmitError("Unable to check username. Please try again.");
            return;
        }

        if (usernameStatus !== "available"){
            setSubmitError("Please choose an available username.");
            return;
        }

        if (!emailIsValid){
            setSubmitError('Please enter a valid email address');
            return;
        }

        if (/\s/.test(password)){
            setSubmitError("Password must not contain spaces.");
            return;
        }

        if (
            !passwordRules.length ||
            !passwordRules.uppercase ||
            !passwordRules.lowercase ||
            !passwordRules.number ||
            !passwordRules.special ||
            !passwordRules.noSpaces
        ){
            setSubmitError("Please fix the password requirements.");
            return;
        }

        if (password !== confirmPassword){
            setSubmitError("Passwords do not match.");
            return;
        }

        console.log("Form submitted")
    }

    useEffect(() => {
        if (!API_BASE_URL) return;

        const controller = new AbortController();

        fetch(`${API_BASE_URL}/health`, {
            signal: controller.signal,
        }).catch(() => {
            // The username check will display an error if the API is unavailable.
        });

        return () => controller.abort();
    }, []);

    useEffect(() => {
        const controller = new AbortController();
        let timedOut = false;
        let timeoutId: ReturnType<typeof setTimeout> | undefined;

        const timer = setTimeout(async () => {

            if (!API_BASE_URL) {
                setUsernameStatus("error");
                return;
            }

            if (username.length < 5 || !usernameIsValid){
                setUsernameStatus("idle");
                return;
            }

            timeoutId = setTimeout(() => {
                timedOut = true;
                controller.abort();
            }, 45000);

            try {
                const response = await fetch(
                    `${API_BASE_URL}/check-username?username=${encodeURIComponent(username)}`,
                { signal: controller.signal }
                );

                if (!response.ok){
                    throw new Error("Failed to check username");
                }

                const data = await response.json();

                setUsernameStatus(
                    data.available ? "available" : "taken"
                );

            } catch (error) {
                if (error instanceof DOMException && error.name === "AbortError"){
                    if (timedOut) {
                        setUsernameStatus("error");
                    }
                    return;
                }

                setUsernameStatus("error");
            } finally {
                clearTimeout(timeoutId);
            }

        }, 400);

        return () => {
            clearTimeout(timer);
            clearTimeout(timeoutId);
            controller.abort();
        };
    }, [username, usernameIsValid, usernameCheckAttempt]);

  return (
    <div className="register-page">

        <div className='brand'>
            <span className='logo-icon'>ET</span>
            <span>Expense Tracker</span>
        </div>

        <h2>Create your account</h2>
        <p>Start tracking your expenses in minutes</p>

        <div className="login-container">

            <form onSubmit={handleSubmit} noValidate>
                <div>
                    <label htmlFor='username'>Username</label>

                    <input
                        id="username"
                        aria-invalid={touched.username && username.length > 0 && !usernameIsValid}
                        type="text"
                        placeholder='e.g. akash_s'
                        value={username}
                        onChange={(e) => {
                            setSubmitError("");
                            const value = e.target.value;
                            setUsername(value);

                            if (USERNAME_PATTERN.test(value)) {
                                setUsernameStatus("checking");
                            } else {
                                setUsernameStatus("idle");
                            }
                        }}

                        onBlur={() => setTouched(prev => ({ ...prev, username:true}))}
                        minLength={5}
                        maxLength={20}
                        spellCheck={false}
                        autoComplete='username'
                        required
                    />

                    <div aria-live='polite' aria-atomic="true">
                        {touched.username && username.length > 0 && !usernameIsValid && (
                            <p className='username-error'>
                                Username must be 5-20 characters and contain only letters,
                                numbers, and underscores
                            </p>
                        )}

                        {usernameIsValid && usernameStatus === "checking" && (
                            <p className='username-checking'>
                                Checking username...
                            </p>
                        )}

                        {usernameIsValid && usernameStatus === "available" && (
                            <p className="username-available">
                                ✓ Username available
                            </p>
                        )}

                        {usernameIsValid && usernameStatus === "taken" && (
                            <p className="username-taken">
                                ✕ Username already taken
                            </p>
                        )}

                        {usernameIsValid && usernameStatus === "error" && (
                            <p className="username-error">
                                Unable to check username. {" "}
                                <button
                                    type='button'
                                    onClick={() => {
                                        setUsernameStatus("checking")
                                        setUsernameCheckAttempt(prev => prev + 1);
                                    }}
                                >
                                    Try again
                                </button>
                            </p>
                        )}
                    </div>
                </div>

                <div>
                    <label htmlFor="email">Email</label>

                    <input
                        id='email'
                        type="email"
                        aria-invalid={touched.email && email.length > 0 && !emailIsValid}
                        value = {email}
                        onChange={(e) => {
                            setSubmitError("");
                            setEmail(e.target.value);
                        }}
                        placeholder='you@example.com'
                        autoComplete='email'
                        maxLength={254}
                        onBlur={() => setTouched(prev => ({ ...prev, email: true}))}
                        required
                    />

                    <div aria-live='polite' aria-atomic='true'>
                        {touched.email && email.length > 0 && !emailIsValid && (
                            <p className='email-error'>
                                Please enter a valid email address.
                            </p>
                        )}
                    </div>

                </div>

                <div>
                    <label htmlFor="password">Password</label>

                    <div className='password-input-wrapper'>
                        <input
                            id="password"
                            aria-invalid={
                                touched.password && password.length > 0 &&
                                Object.values(passwordRules).some(rule => !rule)
                            }
                            value = {password}
                            onChange={(e) => {
                                setSubmitError("");
                                setPassword(e.target.value);
                            }}
                            type={showPassword ? "text": "password"}
                            placeholder='Min. 8 characters'
                            minLength={8}
                            maxLength={64}
                            autoComplete='new-password'
                            onFocus={() => setFocusedField("password")}
                            onBlur={() => {
                                setFocusedField(null);
                                setTouched(prev => ({ ...prev, password: true}));
                            }}
                            required
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

                    {(
                        focusedField === "password" ||
                        touched.password && Object.values(passwordRules).some(rule => !rule))
                        && (
                        <div className='password-rules'>
                            <p>Password requirements:</p>

                            <div className={passwordRules.length ? "rule-valid" : "rule-invalid"}>
                                {passwordRules.length ? "✓" : "✕"} 8-64 characters
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

                            <div className={passwordRules.noSpaces ? "rule-valid" : "rule-invalid"}>
                                {passwordRules.noSpaces ? "✓" : "✕"} No spaces 
                            </div>

                        </div>
                    )}

                </div>

                <div>
                    <label htmlFor="confirm-password">Confirm Password</label>

                    <div className='password-input-wrapper'>
                        <input
                            id="confirm-password"
                            aria-invalid={
                                touched.confirmPassword && confirmPassword.length > 0 &&
                                password !== confirmPassword
                            }
                            type={showConfirmPassword ? "text": "password"}
                            value={confirmPassword}
                            autoComplete='new-password'
                            onChange={(e) => {
                                setSubmitError("");
                                setConfirmPassword(e.target.value);
                            }}
                            onBlur={() =>
                                setTouched(prev => ({ ...prev, confirmPassword: true}))
                            }
                            placeholder='Re-enter your password'
                            required
                        />

                        <button
                            type='button'
                            className='password-toggle'
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                            aria-label={showConfirmPassword
                                            ? "Hide confirm password"
                                            : "Show confirm password"
                                        }
                            >
                                {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                        </button>

                    </div>

                    <div aria-live='polite' aria-atomic='true'>
                        {(touched.confirmPassword ||
                            confirmPassword.length >= password.length) &&
                            confirmPassword.length > 0 && (
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
                </div>

                {submitError && (
                    <p className='submit-error'>
                        {submitError}
                    </p>
                )}

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