import React from "react";
import { BrowserRouter, Routes as RouterRoutes, Route } from "react-router-dom";
import ScrollToTop from "components/ScrollToTop";
import ErrorBoundary from "components/ErrorBoundary";
import NotFound from "pages/NotFound";
import MainDashboard from './pages/main-dashboard';
import JellyfinStatistics from './pages/jellyfin-statistics';
import InitialConfiguration from './pages/initial-configuration';
import Library from './pages/library';
import Monitoring from './pages/monitoring';
import MediaDetail from './pages/media-detail';
import JellyseerrRequests from './pages/jellyseerr-requests';
import Calendar from './pages/calendar';

const Routes = () => {
  return (
    <BrowserRouter>
      <ErrorBoundary>
      <ScrollToTop />
      <RouterRoutes>
        {/* Define your route here */}
        <Route path="/" element={<InitialConfiguration />} />
        <Route path="/main-dashboard" element={<MainDashboard />} />
        <Route path="/jellyfin-statistics" element={<JellyfinStatistics />} />
        <Route path="/initial-configuration" element={<InitialConfiguration />} />
        <Route path="/library" element={<Library />} />
        <Route path="/media-detail" element={<MediaDetail />} />
        <Route path="/monitoring" element={<Monitoring />} />
        <Route path="/jellyseerr-requests" element={<JellyseerrRequests />} />
        <Route path="/calendar" element={<Calendar />} />
        <Route path="*" element={<NotFound />} />
      </RouterRoutes>
      </ErrorBoundary>
    </BrowserRouter>
  );
};

export default Routes;
