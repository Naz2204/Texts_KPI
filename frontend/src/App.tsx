import { createBrowserRouter, RouterProvider } from 'react-router';
import MainPage from './pages/MainPage/MainPage';
import BaseLayout from './layouts/BaseLayout';
import { QueryClientProvider } from '@tanstack/react-query';
import ResultPage from './pages/ResultPage';
import { getAnalyzedFileLoader } from './queries/loaders';
import { queryClient } from './queries';

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
