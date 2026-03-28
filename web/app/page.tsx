'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import './auth.css';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.error || 'Erro ao autenticar');
        return;
      }

      // Store token and redirect
      if (data.token) {
        localStorage.setItem('authToken', data.token);
        localStorage.setItem('userEmail', email);
        router.push('/dashboard');
      } else {
        setMessage(data.message || 'Verifique seu email para confirmar');
      }
    } catch (error) {
      setMessage('Erro ao conectar com o servidor');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>CRO Analyzer</h1>
          <p>Otimização de Taxa de Conversão Automática</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              placeholder="seu@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Senha</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {message && (
            <div className={`message ${isLogin ? 'error' : 'success'}`}>
              {message}
            </div>
          )}

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Carregando...' : isLogin ? 'Entrar' : 'Registrar'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            {isLogin ? 'Não tem conta?' : 'Já tem conta?'}{' '}
            <button
              type="button"
              className="link-button"
              onClick={() => {
                setIsLogin(!isLogin);
                setMessage('');
              }}
            >
              {isLogin ? 'Registre-se' : 'Entre'}
            </button>
          </p>
        </div>

        <div className="auth-features">
          <div className="feature">
            <span className="icon">📊</span>
            <p>Análise em Tempo Real</p>
          </div>
          <div className="feature">
            <span className="icon">🤖</span>
            <p>Recomendações Automáticas</p>
          </div>
          <div className="feature">
            <span className="icon">📈</span>
            <p>Histórico Completo</p>
          </div>
        </div>
      </div>
    </div>
  );
}
