import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { register } from '../store/authAPI'; // Import your register action
import { Link } from 'react-router-dom'; // Import Link from react-router-dom

function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const dispatch = useDispatch();
  const authStatus = useSelector((state) => state.auth.status);

  const handleSubmit = (e) => {
    e.preventDefault();
    dispatch(register({ username, email, password1, password2 })); // Call your register action
  };

  if (authStatus === 'loading') return <div className="loading-message">Registering...</div>;

  return (
    <form onSubmit={handleSubmit} className="register-form"> {/* Apply the CSS class */}
      <h2>Register</h2>
      <div>
        <label>Username:</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
      </div>
      <div>
        <label>Email:</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" value={password1} onChange={(e) => setPassword1(e.target.value)} />
      </div>
      <div>
        <label>Repeat Password:</label>
        <input type="password" value={password2} onChange={(e) => setPassword2(e.target.value)} />
      </div>
      <button type="submit">Register</button>
      <p>
        Already have an account? <Link to="/">Login here</Link>
      </p> {/* Link to login page */}
    </form>
  );
}

export default Register;
