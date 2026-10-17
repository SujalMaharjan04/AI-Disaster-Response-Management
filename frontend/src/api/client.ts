import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE,
});

export const uploadImage = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const fetchResults = async (requestId: number) => {
  const response = await api.get(`/results/${requestId}`);
  return response.data;
};
