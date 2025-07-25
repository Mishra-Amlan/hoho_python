// Python FastAPI Backend Starter for Replit
// Express has been completely removed - this proxies to Python backend

import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { spawn } from 'child_process';
import { execSync } from 'child_process';
import path from 'path';

const app = express();
const PORT = process.env.PORT || 5002;

console.log('🚀 Hotel Audit System - Python Backend with Proxy');
console.log('==================================================');

// Kill any existing Python processes
try {
  console.log('🔧 Cleaning up existing processes...');
  execSync('pkill -f "python.*main.py" || true', { stdio: 'ignore' });
  execSync('pkill -f "uvicorn" || true', { stdio: 'ignore' });
} catch (error) {
  // Ignore cleanup errors
}

console.log('🐍 Starting Python FastAPI server...');

// Start the Python backend
const pythonProcess = spawn('python', ['main.py'], {
  cwd: 'python_backend',
  stdio: 'pipe'
});

let pythonReady = false;

pythonProcess.stdout?.on('data', (data) => {
  const output = data.toString();
  console.log(output);
  if (output.includes('Uvicorn running')) {
    pythonReady = true;
    console.log('✅ Python backend is ready');
  }
});

pythonProcess.stderr?.on('data', (data) => {
  console.error('Python Error:', data.toString());
});

// Serve static files with proper MIME types
app.use(express.static(path.join(process.cwd(), 'dist/public'), {
  setHeaders: (res, filePath) => {
    if (filePath.endsWith('.js')) {
      res.setHeader('Content-Type', 'application/javascript');
    } else if (filePath.endsWith('.css')) {
      res.setHeader('Content-Type', 'text/css');
    } else if (filePath.endsWith('.html')) {
      res.setHeader('Content-Type', 'text/html');
    }
  }
}));

// Proxy API requests to Python backend
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:8000',
  changeOrigin: true,
  pathRewrite: {
    '^/api': '/api'
  },
  onError: (err, req, res) => {
    console.error('Proxy Error:', err.message);
    res.status(500).json({ 
      error: 'Python backend not available',
      message: 'Make sure Python FastAPI server is running on port 8000'
    });
  }
}));

// Serve React app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(process.cwd(), 'dist/public/index.html'));
});

// Start the proxy server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🌐 Proxy server running on http://0.0.0.0:${PORT}`);
  console.log(`🔗 API proxying to Python backend on port 8000`);
  console.log(`📍 Frontend served from client/ directory`);
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down...');
  pythonProcess.kill('SIGINT');
  process.exit(0);
});

process.on('SIGTERM', () => {
  pythonProcess.kill('SIGTERM');
  process.exit(0);
});