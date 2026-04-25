import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const askQuestion = async (question) => {
  const response = await api.post('/ask', { question });
  return response.data;
};

export const getTables = async () => {
  const response = await api.get('/tables');
  return response.data;
};

export const indexSchemas = async () => {
  const response = await api.post('/index');
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
