import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { login, register as registerAPI } from './authAPI';


const initialState = {
  isAuthenticated: false,
  token: null,
  status: 'idle', // idle | loading | succeeded | failed
  error: null,
};

// Create an async thunk for registration
export const register = createAsyncThunk('auth/register', async (userData) => {
  const response = await registerAPI(userData);
  return response.data;
});

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout(state) {
      state.isAuthenticated = false;
      state.token = null;
    },
    setCredentials(state, action) {
      state.isAuthenticated = true;
      state.token = action.payload.token;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(login.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.isAuthenticated = true;
        state.token = action.payload.token;
      })
      .addCase(login.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      .addCase(register.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(register.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.isAuthenticated = true;
        state.token = action.payload.token; // Adjust based on your API response
      })
      .addCase(register.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  },
});

export const { logout, setCredentials } = authSlice.actions;

export default authSlice.reducer;
