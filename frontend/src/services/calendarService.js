import servarrHubClient from '../lib/servarrHubClient';

/**
 * Get all calendar events (upcoming releases)
 * @returns {Promise<Array>} Array of calendar events
 */
export const getCalendarEvents = async (days = 7) => {
  try {
    const response = await servarrHubClient?.get(`/dashboard/calendar?days=${days}`);
    
    // Map snake_case API response to camelCase for frontend
    const events = response?.data?.map(event => ({
      id: event?.id,
      title: event?.title,
      mediaType: event?.media_type,
      releaseDate: event?.release_date,
      imageUrl: event?.image_url,
      imageAlt: event?.image_alt,
      episode: event?.episode,
      status: event?.status
    })) || [];
    
    return events;
  } catch (error) {
    return [];
  }
};

/**
 * Add new calendar event
 * @param {Object} event - Calendar event data
 * @returns {Promise<Object|null>} Created calendar event or null
 */
export const addCalendarEvent = async (event) => {
  try {
    const response = await servarrHubClient?.post('/calendar/events', event);
    return response?.data || null;
  } catch (error) {
    return null;
  }
};

/**
 * Update calendar event status
 * @param {string} id - Calendar event ID
 * @param {string} status - New status
 * @returns {Promise<boolean>} Success status
 */
export const updateCalendarEventStatus = async (id, status) => {
  try {
    await servarrHubClient?.patch(`/calendar/events/${id}`, { status });
    return true;
  } catch (error) {
    return false;
  }
};

/**
 * Delete calendar event
 * @param {string} id - Calendar event ID
 * @returns {Promise<boolean>} Success status
 */
export const deleteCalendarEvent = async (id) => {
  try {
    await servarrHubClient?.delete(`/calendar/events/${id}`);
    return true;
  } catch (error) {
    return false;
  }
};