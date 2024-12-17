const { execSync } = require('child_process');

console.log('Setting up a new Next.js project with TypeScript...');

// Create a new Next.js project with TypeScript
execSync('npx create-next-app@latest script-feedback-app --typescript --eslint --tailwind --app --src-dir --import-alias "@/*"', { stdio: 'inherit' });

console.log('Changing to the project directory...');
process.chdir('script-feedback-app');

console.log('Installing shadcn/ui...');
execSync('npx shadcn@latest init', { stdio: 'inherit' });

console.log('Installing required shadcn/ui components...');
execSync('npx shadcn@latest add button textarea tabs', { stdio: 'inherit' });

console.log('Project setup complete!');
console.log('To start your development server, run:');
console.log('cd script-feedback-app');
console.log('npm run dev');