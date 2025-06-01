import { createBrowserRouter, RouterProvider } from 'react-router';
import MainPage from './pages/MainPage/MainPage';
import BaseLayout from './layouts/BaseLayout';
import { QueryClientProvider } from '@tanstack/react-query';
import { getAnalyzedFileLoader, queryClient } from './queries/store';
import ResultPage from './pages/ResultPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <BaseLayout />,
    children: [{ index: true, element: <MainPage /> }]
  },
  {
    path: '/:id',
    element: <ResultPage />,
    loader: getAnalyzedFileLoader
  }
]);

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}
