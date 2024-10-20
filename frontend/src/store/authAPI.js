import { createAsyncThunk } from '@reduxjs/toolkit';

import api from './api';

export const login = createAsyncThunk('auth/login', async (credentials) => {
  const response = await api.post('api/user/login/', credentials);
  return response.data;  
});


export const register = createAsyncThunk(
  'auth/register',
  async (credentials) => {
    const response = await api.post('api/user/register/', credentials);
    return response.data;
  }
)

