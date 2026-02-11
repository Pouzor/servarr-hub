import servarrHubClient from '../lib/servarrHubClient';

/**
 * Dashboard Statistics Operations
 */

// Get all dashboard statistics
export const getDashboardStatistics = async () => {
  try {
    const response = await servarrHubClient?.get('/dashboard/statistics');
    return response?.data || [];
  } catch (error) {
    // Silently handle errors - API might be down or endpoint not implemented
    return [];
  }
};

// Get single statistic by type
export const getDashboardStatistic = async (statType) => {
  try {
    const response = await servarrHubClient?.get(`/dashboard/statistics/${statType}`);
    return response?.data || null;
  } catch (error) {
    return null;
  }
};

// Get recent library additions
export const getRecentItems = async (limit = 20) => {
  try {
    const response = await servarrHubClient?.get(`/dashboard/recent-items?limit=${limit}`);
    return response?.data || [];
  } catch (error) {
    return [];
  }
};

// Save or update dashboard statistic
export const saveDashboardStatistic = async (statType, totalCount, details) => {
  try {
    const response = await servarrHubClient?.post('/dashboard/statistics', {
      statType,
      totalCount,
      details,
      lastSynced: new Date()?.toISOString()
    });
    return response?.data || null;
  } catch (error) {
    console.error('Error saving dashboard statistic:', error?.message);
    throw error;
  }
};

// Bulk update dashboard statistics
export const bulkUpdateDashboardStatistics = async (statistics) => {
  try {
    const response = await servarrHubClient?.post('/dashboard/statistics/bulk', {
      statistics
    });
    return response?.data || [];
  } catch (error) {
    console.error('Error bulk updating dashboard statistics:', error?.message);
    throw error;
  }
};

export default {
  getDashboardStatistics,
  getDashboardStatistic,
  saveDashboardStatistic,
  bulkUpdateDashboardStatistics
};