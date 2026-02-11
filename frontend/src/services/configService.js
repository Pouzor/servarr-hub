import servarrHubClient from '../lib/servarrHubClient';

/**
 * Service Configuration Operations
 */

// Helper function to convert API response to camelCase
const mapServiceResponse = (data) => {
  if (!data) return null;
  
  return {
    serviceName: data?.service_name,
    url: data?.url,
    apiKey: data?.api_key,
    username: data?.username,
    password: data?.password,
    port: data?.port,
    isActive: data?.is_active,
    id: data?.id,
    lastTestedAt: data?.last_tested_at,
    testStatus: data?.test_status,
    testMessage: data?.test_message,
    createdAt: data?.created_at,
    updatedAt: data?.updated_at
  };
};

// Get all service configurations
export const getServiceConfigurations = async () => {
  try {
    // Fetch all services individually since the API uses /api/services/{service_name}
    const serviceNames = ['jellyfin', 'jellyseerr', 'radarr', 'sonarr', 'qbittorrent'];
    const promises = serviceNames?.map(name => 
      servarrHubClient?.get(`/services/${name}`)?.then(response => mapServiceResponse(response?.data))?.catch(error => {
          // If service not found (404), return null
          if (error?.response?.status === 404) {
            return null;
          }
          throw error;
        })
    );
    
    const results = await Promise?.all(promises);
    return results?.filter(config => config !== null);
  } catch (error) {
    console.error('Error fetching service configurations:', error?.message);
    return [];
  }
};

// Get single service configuration by service name
export const getServiceConfiguration = async (serviceName) => {
  try {
    const response = await servarrHubClient?.get(`/services/${serviceName}`);
    return mapServiceResponse(response?.data);
  } catch (error) {
    console.error(`Error fetching ${serviceName} configuration:`, error?.message);
    return null;
  }
};

export const saveServiceConfiguration = async (serviceName, config) => {
  try {
    const response = await servarrHubClient?.put(`/services/${serviceName}`, {
      service_name: serviceName,
      url: config?.url,
      api_key: config?.apiKey,
      username: config?.username,
      password: config?.password,
      port: config?.port ? parseInt(config?.port) : null,
      is_active: config?.isActive !== undefined ? config?.isActive : false,
      last_tested_at: config?.lastTestedAt || null,
      test_status: config?.testStatus || null,
      test_message: config?.testMessage || null
    });
    return mapServiceResponse(response?.data);
  } catch (error) {
    console.error(`Error saving ${serviceName} configuration:`, error?.message);
    throw error;
  }
};


// Test service connection
export const testServiceConnection = async (serviceName) => {
  try {
    const response = await servarrHubClient?.post(`/services/${serviceName}/test`, {});
    return {
      success: response?.data?.success,
      message: response?.data?.message,
      testedAt: response?.data?.tested_at
    };
  } catch (error) {
    console.error(`Error testing ${serviceName} connection:`, error?.message);
    throw error;
  }
};

// Update test status for a service
export const updateServiceTestStatus = async (serviceName, testStatus, testMessage) => {
  try {
    const response = await servarrHubClient?.patch(`/services/${serviceName}/test`, {
      test_status: testStatus,
      test_message: testMessage,
      last_tested_at: new Date()?.toISOString()
    });
    return mapServiceResponse(response?.data);
  } catch (error) {
    console.error('Error updating test status:', error?.message);
    throw error;
  }
};

// Delete service configuration
export const deleteServiceConfiguration = async (serviceName) => {
  try {
    await servarrHubClient?.delete(`/services/${serviceName}`);
    return true;
  } catch (error) {
    console.error('Error deleting service configuration:', error?.message);
    return false;
  }
};

export default {
  getServiceConfigurations,
  getServiceConfiguration,
  saveServiceConfiguration,
  testServiceConnection,
  updateServiceTestStatus,
  deleteServiceConfiguration
};