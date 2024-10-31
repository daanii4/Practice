import React, { useEffect, useState } from 'react';
import { fetchAllUsers, deleteUser, updateUserRole } from '../services/api';

const AdminPanel = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch users when the component is mounted
  useEffect(() => {
    const fetchUsers = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await fetchAllUsers(token);
          setUsers(response.data);
        } catch (error) {
          console.error('Error fetching users:', error);
          setError('Error fetching users');
        } finally {
          setLoading(false);
        }
      } else {
        setError('No token found');
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  // Handle user deletion
  const handleDelete = async (userId) => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        await deleteUser(userId, token);
        setUsers(users.filter((user) => user.id !== userId)); // Remove the deleted user from the state
      } catch (error) {
        console.error('Error deleting user:', error);
        setError('Error deleting user');
      }
    }
  };

  // Handle promoting a user to admin
  const handlePromoteToAdmin = async (userId) => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        await updateUserRole(userId, { is_admin: true }, token);
        // Update the state to reflect the user's new admin status
        setUsers(users.map((user) => (user.id === userId ? { ...user, is_admin: true } : user)));
      } catch (error) {
        console.error('Error promoting user to admin:', error);
        setError('Error promoting user to admin');
      }
    }
  };

  // Render the loading state
  if (loading) {
    return <div>Loading users...</div>;
  }

  // Render the error state
  if (error) {
    return <div>{error}</div>;
  }

  // Render the list of users
  return (
    <div>
      <h2>Admin Panel - User Management</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{`${user.first_name} ${user.last_name}`}</td>
              <td>{user.email}</td>
              <td>{user.is_admin ? 'Admin' : 'User'}</td>
              <td>
                <button onClick={() => handleDelete(user.id)}>Delete</button>
                {!user.is_admin && (
                  <button onClick={() => handlePromoteToAdmin(user.id)}>Promote to Admin</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminPanel;
