
/**
 * App.tsx
 *
 * Main entry component of the Knowledge Islands frontend.
 *
 * Responsibilities:
 * - Defines the main application structure.
 * - Displays the welcome message.
 * * Future development:
 * - Integrate the island map.
 * - Display learning missions and quizzes.
 * - Connect the frontend to the backend API.
 */

// Import the CSS file responsible for styling this component.
import './App.css'

/**
 * App component
 *
 * This is the root React component of our application.
 * React components are JavaScript/TypeScript functions
 * that return JSX to describe the user interface.
 */
function App() {
  return (
    // <main> represents the main content of the application.
    <main>
      {/* Main title of our educational game. */}
      <h1>Knowledge Islands</h1>

      {/* Short welcome message displayed below the title. */}
      <p>Welcome to your learning adventure!</p>
    </main>
  )
}

// Export the component so it can be imported into main.tsx.
export default App
