import React from 'react';
import Icon from '../../../components/AppIcon';

const ServerPerformancePanel = ({ performanceData, isLoading }) => {
  const MetricCard = ({ icon, label, value, unit, status, percentage }) => (
    <div className="bg-muted/30 rounded-lg p-3 md:p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Icon name={icon} size={16} color={`var(--color-${status})`} />
          <span className="text-xs text-muted-foreground">{label}</span>
        </div>
        <span className={`text-xs font-semibold px-2 py-0.5 rounded bg-${status}/10 text-${status}`}>
          {status?.toUpperCase()}
        </span>
      </div>
      <div className="flex items-baseline gap-2">
        <span className="text-xl md:text-2xl font-bold text-foreground">{value}</span>
        <span className="text-sm text-muted-foreground">{unit}</span>
      </div>
      {percentage !== undefined && (
        <div className="mt-2">
          <div className="w-full bg-muted rounded-full h-1.5">
            <div 
              className={`bg-${status} rounded-full h-1.5 transition-all duration-500`}
              style={{ width: `${percentage}%` }}
            ></div>
          </div>
        </div>
      )}
    </div>
  );

  if (isLoading) {
    return (
      <div className="bg-card border border-border rounded-lg p-4 md:p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-accent/10 flex items-center justify-center">
            <Icon name="Server" size={20} color="var(--color-accent)" />
          </div>
          <div>
            <h3 className="text-base md:text-lg font-semibold text-foreground">Server Performance</h3>
            <p className="text-xs md:text-sm text-muted-foreground">Real-time system metrics</p>
          </div>
        </div>
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-lg bg-accent/10 flex items-center justify-center">
          <Icon name="Server" size={20} color="var(--color-accent)" />
        </div>
        <div>
          <h3 className="text-base md:text-lg font-semibold text-foreground">Server Performance</h3>
          <p className="text-xs md:text-sm text-muted-foreground">Real-time system metrics</p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <MetricCard
          icon="Cpu"
          label="CPU Usage"
          value={performanceData?.cpuUsage}
          unit="%"
          status={performanceData?.cpuStatus || 'success'}
          percentage={performanceData?.cpuUsage}
        />
        <MetricCard
          icon="HardDrive"
          label="Memory Usage"
          value={performanceData?.memoryUsage}
          unit={performanceData?.memoryUnit || 'GB'}
          status={performanceData?.memoryStatus || 'success'}
          percentage={(() => {
            const usage = performanceData?.memoryUsage || 0;
            const total = performanceData?.totalMemory || 1;
            const usageUnit = performanceData?.memoryUnit;
            const totalUnit = performanceData?.totalMemoryUnit;
            
            // Convert to same unit for percentage calculation
            let usageInMB = usage;
            let totalInMB = total;
            
            if (usageUnit === 'GB') usageInMB = usage * 1024;
            if (totalUnit === 'GB') totalInMB = total * 1024;
            
            return (usageInMB / totalInMB) * 100;
          })()}
        />
        <MetricCard
          icon="Wifi"
          label="Bandwidth"
          value={performanceData?.bandwidth}
          unit="Mbps"
          status={performanceData?.bandwidthStatus || 'success'}
          percentage={(performanceData?.bandwidth / performanceData?.maxBandwidth) * 100}
        />
        <MetricCard
          icon="Database"
          label="Storage Used"
          value={performanceData?.storageUsed}
          unit={performanceData?.storageUnit || 'TB'}
          status={performanceData?.storageStatus || 'success'}
          percentage={(() => {
            const used = performanceData?.storageUsed || 0;
            const total = performanceData?.totalStorage || 1;
            const usedUnit = performanceData?.storageUnit;
            
            // If storage is in GB but total might be in TB, convert
            let usedInGB = used;
            let totalInGB = total;
            
            if (usedUnit === 'TB') usedInGB = used * 1024;
            // Assuming totalStorage is always in same unit as storageUsed after formatting
            
            return (usedInGB / totalInGB) * 100;
          })()}
        />
      </div>
      <div className="bg-muted/30 rounded-lg p-4">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-sm font-semibold text-foreground">Active Transcoding Sessions</h4>
          <span className="text-xs font-semibold px-2 py-1 rounded bg-primary/10 text-primary">
            {performanceData?.activeTranscodes} Active
          </span>
        </div>
        
        <div className="space-y-3">
          {performanceData?.transcodingSessions?.map((session, index) => (
            <div key={index} className="flex items-center justify-between p-2 bg-background rounded-lg">
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-foreground truncate">{session?.title}</p>
                <p className="text-xs text-muted-foreground">
                  {session?.user} • {session?.quality} → {session?.targetQuality}
                </p>
              </div>
              <div className="flex items-center gap-2 ml-3">
                <div className="text-right">
                  <p className="text-xs font-semibold text-foreground">{session?.progress}%</p>
                  <p className="text-xs text-muted-foreground">{session?.speed}x</p>
                </div>
                <div className="w-12 h-12 rounded-lg bg-muted flex items-center justify-center">
                  <Icon name="Film" size={20} color="var(--color-primary)" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ServerPerformancePanel;