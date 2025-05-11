# Netscan Frontend

This repository contains the frontend application for Netscan, a network scanning and monitoring tool. Built with React and Vite, it offers a responsive and modern user interface.

##  Getting Started

### Prerequisites

Ensure you have the following installed:

- **Node.js** (v23.11.0 or later)
- **npm** (v10.9.2 or later)

---

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/dimastack/netscan.git
cd netscan/frontend
npm install
```

---

## Development

Start the development server:

```bash
npm run dev
```
Open your browser and navigate to http://localhost:5173 to view the application.

**Features**:
- **Authentication**: Login and Register forms with validation.
- **Routing**: Protected routes using React Router.
- **State Management**: Local state for form handling and error messages.
- **Styling**: Global CSS with responsive design.

---

## Folder Structure

```md
frontend/
├── app/
│   ├── public/                # Static assets like images and icons
│   ├── src/
│   │   ├── api/               # API service modules
│   │   ├── components/        # Reusable UI components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── pages/             # Page components (Login, Register, Dashboard)
│   │   ├── router/            # React Router setup
│   │   ├── services/          # Client-side services
│   │   ├── styles/            # Global and component-specific styles
│   │   ├── utils/             # Utility functions
│   │   ├── App.jsx            # Main application component
│   │   └── main.jsx           # Entry point for React
│   ├── .env                   # Environment variables
│   ├── .gitignore             # Git ignore rules
│   ├── eslint.config.js       # ESLint configuration
│   ├── index.html             # Main HTML template
│   ├── package.json           # Project metadata and dependencies
│   └── vite.config.js         # Vite configuration
└── Dockerfile                 # Docker configuration for deployment

```

---

## Key Components
- App.jsx: The root component that sets up routing and layout.
- main.jsx: The entry point that renders the app into the DOM.
- PrimaryButton.jsx: A reusable button component with consistent styling.
- Loader.jsx: A loading spinner component displayed during asynchronous operations.
- FormWrapper.jsx: A base form component used by both Login and Register pages.
- Login.jsx & Register.jsx: Page components that utilize AuthForm.jsx for user authentication.

---
