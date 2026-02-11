import servarrHubClient from '../lib/servarrHubClient';

/**
 * Get all Jellyseerr requests
 * @returns {Promise<Array>} Array of requests
 */
export const getJellyseerrRequests = async (status = 'pending', limit = 10) => {
  try {
    const response = await servarrHubClient?.get(`/dashboard/requests?status=${status}&limit=${limit}`);
    
    // Map snake_case API response to camelCase for frontend
    const requests = response?.data?.map(request => ({
      id: request?.id,
      title: request?.title,
      mediaType: request?.media_type, // 'movie' or 'tv'
      requestedBy: request?.requested_by,
      requestedDate: request?.requested_date,
      status: request?.status, // 1 = approved, 0 = pending
      imageUrl: request?.image_url,
      imageAlt: request?.image_alt,
      year: request?.year,
      description: request?.description,
      priority: request?.priority,
      quality: request?.quality
    })) || [];
    
    return requests;
  } catch (error) {
    return [];
  }
};

/**
 * Add new Jellyseerr request
 * @param {Object} request - Request data
 * @returns {Promise<Object|null>} Created request or null
 */
export const addJellyseerrRequest = async (request) => {
  try {
    const response = await servarrHubClient?.post('/jellyseerr/requests', request);
    return response?.data || null;
  } catch (error) {
    return null;
  }
};

/**
 * Delete Jellyseerr request (approve/reject)
 * @param {string} id - Request ID
 * @returns {Promise<boolean>} Success status
 */
export const deleteJellyseerrRequest = async (id) => {
  try {
    await servarrHubClient?.delete(`/jellyseerr/requests/${id}`);
    return true;
  } catch (error) {
    return false;
  }
};

/**
 * Update request priority
 * @param {string} id - Request ID
 * @param {string} priority - New priority
 * @returns {Promise<boolean>} Success status
 */
export const updateRequestPriority = async (id, priority) => {
  try {
    await servarrHubClient?.patch(`/jellyseerr/requests/${id}`, { priority });
    return true;
  } catch (error) {
    return false;
  }
};