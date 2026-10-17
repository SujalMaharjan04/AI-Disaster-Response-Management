import { useState, useEffect } from 'react';
import { uploadImage, fetchResults } from '../api/client';

export type AnalysisState = 'IDLE' | 'UPLOADING' | 'PROCESSING' | 'COMPLETED' | 'ERROR';

export function useAnalysis() {
  const [state, setState] = useState<AnalysisState>('IDLE');
  const [requestId, setRequestId] = useState<number | null>(null);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const upload = async (file: File) => {
    try {
      setState('UPLOADING');
      setError(null);
      const data = await uploadImage(file);
      setRequestId(data.request_id);
      setState('PROCESSING');
      setupWebSocket(data.request_id);
    } catch (e: any) {
      setError(e.message || 'Upload failed');
      setState('ERROR');
    }
  };

  const setupWebSocket = (id: number) => {
    const ws = new WebSocket(`ws://localhost:8000/api/ws/${id}`);

    ws.onmessage = async (event) => {
      const msg = JSON.parse(event.data);
      if (msg.event === 'analysis_completed') {
        setResult(msg.data);
        setState('COMPLETED');
        ws.close();
      }
    };

    ws.onerror = () => {
      setError('WebSocket connection error');
      setState('ERROR');
    };
  };

  return { state, requestId, result, error, upload };
}
