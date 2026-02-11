import servarrHubClient from '../lib/servarrHubClient';

/**
 * Sync Metadata Operations
 */

// Get all sync metadata
export const getAllSyncMetadata = async () => {
  try {
    const response = await servarrHubClient?.get('/sync/metadata');
    return response?.data || [];
  } catch (error) {
    console.error('Error fetching sync metadata:', error?.message);
    return [];
  }
};

// Get sync metadata for a specific service
export const getSyncMetadata = async (serviceName) => {
  try {
    const response = await servarrHubClient?.get(`/sync/metadata/${serviceName}`);
    return response?.data || null;
  } catch (error) {
    console.error(`Error fetching sync metadata for ${serviceName}:`, error?.message);
    return null;
  }
};

// Update sync status
export const updateSyncStatus = async (serviceName, status, errorMessage = null) => {
  try {
    const response = await servarrHubClient?.post('/sync/status', {
      serviceName,
      status,
      errorMessage,
      lastSyncTime: status === 'in_progress' ? new Date()?.toISOString() : undefined
    });
    return response?.data || null;
  } catch (error) {
    console.error('Error updating sync status:', error?.message);
    throw error;
  }
};

// Complete sync with results
export const completeSyncMetadata = async (serviceName, recordsSynced, durationMs, nextSyncTime) => {
  try {
    const response = await servarrHubClient?.post('/sync/complete', {
      serviceName,
      recordsSynced,
      durationMs,
      nextSyncTime
    });
    return response?.data || null;
  } catch (error) {
    console.error('Error completing sync metadata:', error?.message);
    throw error;
  }
};

// Get services that need syncing
export const getServicesNeedingSync = async () => {
  try {
    const response = await servarrHubClient?.get('/sync/pending');
    return response?.data || [];
  } catch (error) {
    console.error('Error fetching services needing sync:', error?.message);
    return [];
  }
};

// Trigger manual sync for all services
export const triggerSync = async () => {
  try {
    const response = await servarrHubClient?.post('/sync/trigger');
    return response?.data || { success: false };
  } catch (error) {
    console.error('Error triggering sync:', error?.message);
    return { success: false, error: error?.message };
  }
};

export default {
  getAllSyncMetadata,
  getSyncMetadata,
  updateSyncStatus,
  completeSyncMetadata,
  getServicesNeedingSync,
  triggerSync
};