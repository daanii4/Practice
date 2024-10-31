'use client'; 

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

const Projects = () => {
    const [projects, setProjects] = useState([]);
    const [newProjectName, setNewProjectName] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [triggerRefetch, setTriggerRefetch] = useState(0); // Trigger variable
    const router = useRouter(); // Using Next.js router

    useEffect(() => {
        fetchProjects();
    }, [triggerRefetch]); // Depend on triggerRefetch

    const fetchProjects = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const response = await axios.get('http://localhost:8000/projects/', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            setProjects(response.data);
        } catch (err) {
            if (err.response?.status === 404) { 
                setProjects([]); 
            } else {
                setError('Error fetching projects: ' + (err.response?.data?.detail || err.message));
            }
        } finally {
            setLoading(false);
        }
    };

    const handleCreateNewProject = async (e) => {
        e.preventDefault();
        if (!newProjectName.trim()) {
            setError('Please enter a project name.');
            return;
        }
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const response = await axios.post('http://localhost:8000/projects/create/', 
                { 
                    project_name: newProjectName,
                    status: "draft"
                },
                { headers: { 'Authorization': `Bearer ${token}` } }
            );
            const projectId = response.data.id;
            router.push(`/chatbox-prompt?projectId=${projectId}`); // Use router.push for navigation
            setTriggerRefetch(triggerRefetch + 1); // Trigger refetch after creation
        } catch (err) {
            setError('Error creating project: ' + (err.response?.data?.detail || err.message));
        } finally {
            setLoading(false);
        }
    };

    const handleEditProject = (projectId) => {
        router.push(`/edit-ad/${projectId}`); // Use router.push for editing project
    };

    if (loading) {
        return <div className="login-container">Loading...</div>;
    }

    return (
        <div className="login-container projects-page">
            <h2>Your Projects</h2>
            {error && <p className="error">{error}</p>}
            <form onSubmit={handleCreateNewProject} className="mb-4">
                <input
                    type="text"
                    value={newProjectName}
                    onChange={(e) => setNewProjectName(e.target.value)}
                    placeholder="Enter new project name"
                />
                <button type="submit">Create New Project</button>
            </form>
            <div className="project-list">
                <h3>Past Projects</h3>
                {projects.length === 0 ? (
                    <p>No projects found. Create a new one to get started!</p>
                ) : (
                    <ul>
                        {projects.map((project) => (
                            <li key={project.id} className="project-item">
                                <span>{project.project_name}</span>
                                <button onClick={() => handleEditProject(project.id)}>
                                    Edit
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
};

export default Projects;
