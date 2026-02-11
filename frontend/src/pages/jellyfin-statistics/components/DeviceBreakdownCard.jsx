import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import Icon from '../../../components/AppIcon';

const DeviceBreakdownCard = ({ deviceData, isLoading }) => {
  const COLORS = [
    'var(--color-primary)',
    'var(--color-secondary)',
    'var(--color-accent)',
    'var(--color-success)',
    'var(--color-warning)',
    'var(--color-info)',
    'var(--color-error)'
  ];

  // Transform API data to chart format
  const transformedData = deviceData?.map(item => ({
    name: formatDeviceName(item?.device_type),
    value: item?.session_count || 0,
    percentage: item?.percentage || 0,
    deviceType: item?.device_type
  })) || [];

  // Format device type names for display
  function formatDeviceName(deviceType) {
    const nameMap = {
      'web_browser': 'Web Browser',
      'mobile_app': 'Mobile App',
      'smart_tv': 'Smart TV',
      'desktop_app': 'Desktop App',
      'game_console': 'Game Console',
      'streaming_device': 'Streaming Device',
      'other': 'Other'
    };
    return nameMap?.[deviceType] || deviceType;
  }

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload?.length) {
      return (
        <div className="bg-popover border border-border rounded-lg p-3 shadow-lg">
          <p className="text-sm font-semibold text-foreground mb-1">{payload?.[0]?.name}</p>
          <p className="text-xs text-muted-foreground">
            {payload?.[0]?.value} sessions ({payload?.[0]?.payload?.percentage}%)
          </p>
        </div>
      );
    }
    return null;
  };

  const getDeviceIcon = (deviceType) => {
    const icons = {
      'web_browser': 'Globe',
      'mobile_app': 'Smartphone',
      'smart_tv': 'Tv',
      'desktop_app': 'Monitor',
      'game_console': 'Gamepad2',
      'streaming_device': 'Cast',
      'other': 'HelpCircle'
    };
    return icons?.[deviceType] || 'Monitor';
  };

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-lg bg-secondary/10 flex items-center justify-center">
          <Icon name="Monitor" size={20} color="var(--color-secondary)" />
        </div>
        <div>
          <h3 className="text-base md:text-lg font-semibold text-foreground">Device Breakdown</h3>
          <p className="text-xs md:text-sm text-muted-foreground">Playback by device type</p>
        </div>
      </div>
      {isLoading ? (
        <div className="flex items-center justify-center h-64 text-muted-foreground">
          <p className="text-sm">Loading device data...</p>
        </div>
      ) : transformedData?.length > 0 ? (
        <>
          <div className="w-full h-64 mb-6" aria-label="Device Breakdown Pie Chart">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={transformedData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="var(--color-primary)"
                  dataKey="value"
                >
                  {transformedData?.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS?.[index % COLORS?.length]} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-3">
            {transformedData?.map((device, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-muted/30 rounded-lg">
                <div className="flex items-center gap-3">
                  <div 
                    className="w-8 h-8 rounded-lg flex items-center justify-center"
                    style={{ backgroundColor: `${COLORS?.[index % COLORS?.length]}20` }}
                  >
                    <Icon 
                      name={getDeviceIcon(device?.deviceType)} 
                      size={16} 
                      color={COLORS?.[index % COLORS?.length]}
                    />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-foreground">{device?.name}</p>
                    <p className="text-xs text-muted-foreground">{device?.value} sessions</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold text-foreground">{device?.percentage}%</p>
                  <div className="w-16 bg-muted rounded-full h-1.5 mt-1">
                    <div 
                      className="rounded-full h-1.5 transition-all duration-500"
                      style={{ 
                        width: `${device?.percentage}%`,
                        backgroundColor: COLORS?.[index % COLORS?.length]
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      ) : (
        <div className="flex items-center justify-center h-64 text-muted-foreground">
          <p className="text-sm">No device data available</p>
        </div>
      )}
    </div>
  );
};

export default DeviceBreakdownCard;