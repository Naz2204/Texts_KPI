import { Outlet } from 'react-router';
import Header from '../components/Header/Header';

export default function BaseLayout() {
  return (
    <>
      <Header />
      <hr></hr>
      <Outlet />
    </>
  );
}
