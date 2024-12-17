const { execSync } = require('child_process');

console.log('Installing required Python packages...');
execSync('pip install fastapi uvicorn', { stdio: 'inherit' });

console.log('Starting the FastAPI server...');
try {
  execSync('uvicorn backend.main:app --reload', { stdio: 'inherit' });
} catch (error) {
  console.error('Error starting the server:', error);
}