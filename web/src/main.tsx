import React from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./styles.css";
import App from "./App";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CheckIn from "./pages/CheckIn";
import Tasks from "./pages/Tasks";
import ChangePassword from "./pages/ChangePassword";
import ProtectedRoute from "./components/ProtectedRoute";

const router = createBrowserRouter([
  { path: "/login", element: <Login /> },
  {
    path: "/",
    element: <ProtectedRoute />,
    children: [
      {
        path: "/",
        element: <App />,
        children: [
          { path: "/dashboard", element: <Dashboard /> },
          { path: "/checkin", element: <CheckIn /> },
          { path: "/tasks", element: <Tasks /> },
          { path: "/change-password", element: <ChangePassword /> },
          { index: true, element: <Dashboard /> },
        ],
      },
    ],
  },
  { path: "*", element: <Login /> },
]);

createRoot(document.getElementById("root")!).render(<RouterProvider router={router} />);
