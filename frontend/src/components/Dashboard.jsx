import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import api from '../store/api';
import { logout } from '../store/authSlice';

function Dashboard() {
  const dispatch = useDispatch(); // Initialize dispatch
  const token = useSelector((state) => state.auth.token);
  const [credentials, setCredentials] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  const fetchCredentials = async (page) => {
    try {
      setLoading(true);
      const response = await api.get('/api/credentials/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: { q: searchTerm, page: page }
      });

      // Combine new results with existing credentials and filter out duplicates
      setCredentials((prev) => {
        const combined = [...prev, ...response.data.results];
        const unique = Array.from(new Map(combined.map((cred) => [cred._id, cred])).values());
        return unique;
      });

      setHasMore(response.data.results.length > 0);
    } catch (error) {
      console.error('Failed to fetch credentials:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setCredentials([]);
    setPage(1);
    setHasMore(true);
    fetchCredentials(1);
  }, [searchTerm, token]);

  useEffect(() => {
    const handleScroll = () => {
      if (
        window.innerHeight + document.documentElement.scrollTop + 1 >=
        document.documentElement.offsetHeight
      ) {
        if (hasMore && !loading) {
          setPage((prev) => prev + 1);
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [hasMore, loading]);

  useEffect(() => {
    if (page > 1) {
      fetchCredentials(page);
    }
  }, [page]);

  // Logout function
  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Credentials Dashboard</h1>
      <div className="header-container">
        <input
          type="text"
          className="search-input" // Updated class name
          placeholder="Search..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button onClick={handleLogout} className="logout-button">Logout</button> {/* Logout Button */}
      </div>
      <div className="credentials-list">
        {credentials.map((cred) => (
          <div className="credentials-card" key={cred._id}>
            <div className="card-header">Soft: {cred.soft}</div>
            <div className="card-detail"><strong>Host:</strong> {cred.host}</div>
            <div className="card-detail"><strong>Login:</strong> {cred.login}</div>
            <div className="card-detail"><strong>Password:</strong> {cred.password}</div>
          </div>
        ))}
      </div>
      {loading && <p className="loading-message">Loading...</p>}
      {!hasMore && <p className="no-more-message">No more credentials to load.</p>}
    </div>
  );
}

export default Dashboard;
