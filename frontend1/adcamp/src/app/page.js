// src/app/page.js
'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { signInWithGoogle } from '@/lib/firebaseAuth'; // Using absolute import

const LandingContainer = styled.div`
  height: 100vh;
  background: linear-gradient(135deg, #1a237e 0%, #00796b 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  text-align: center;
`;

const HeroText = styled(motion.h1)`
  font-size: 3rem;
  font-family: 'Montserrat', sans-serif;
  margin-bottom: 1rem;
`;

const SubText = styled(motion.p)`
  font-size: 1.2rem;
  margin-bottom: 2rem;
  max-width: 600px;
`;

const Button = styled(motion.button)`
  padding: 0.8rem 2rem;
  font-size: 1rem;
  background-color: #ff7043;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #ff5722;
  }
`;

export default function Home() {
  const router = useRouter();

  const handleLogin = async () => {
    try {
      const token = await signInWithGoogle();
      const response = await fetch('http://localhost:8000/auth/callback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ credential: token }),
      });

      if (!response.ok) {
        throw new Error('Failed to authenticate with the backend');
      }

      const data = await response.json();
      localStorage.setItem('accessToken', data.access_token);
      router.push('/dashboard');
    } catch (error) {
      console.error('Error during authentication:', error.message);
      // You might want to show an error message to the user here
    }
  };

  return (
    <LandingContainer>
      <HeroText
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        Welcome to AdMaster
      </HeroText>

      <SubText
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.2 }}
      >
        The ultimate tool to streamline your ad campaigns. Ready to take your brand to the next level?
      </SubText>

      <Button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={handleLogin}
      >
        Sign in with Google
      </Button>
    </LandingContainer>
  );
}