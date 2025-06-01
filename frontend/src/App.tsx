import { createBrowserRouter, RouterProvider } from 'react-router';
import MainPage from './pages/MainPage';
import BaseLayout from './layouts/BaseLayout';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from './queries/store';

const router = createBrowserRouter([
  {
    path: '/',
    element: <BaseLayout />,
    children: [{ index: true, element: <MainPage /> }]
  }
]);

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />;
    </QueryClientProvider>
  );
}
