import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Icon from '../../../components/AppIcon';

const UsageChart = ({ data, chartType, onChartTypeChange, isLoading }) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload?.length) {
      return (
        <div className="bg-popover border border-border rounded-lg p-3 shadow-lg">
          <p className="text-sm font-semibold text-foreground mb-2">{label}</p>
          {payload?.map((entry, index) => (
            <div key={index} className="flex items-center justify-between gap-4 text-xs">
              <span className="text-muted-foreground">{entry?.name}:</span>
              <span className="font-semibold" style={{ color: entry?.color }}>
                {entry?.value} {entry?.name === 'Hours Watched' ? 'hrs' : 'plays'}
              </span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-secondary/10 flex items-center justify-center">
            <Icon name="BarChart3" size={20} color="var(--color-secondary)" />
          </div>
          <div>
            <h3 className="text-base md:text-lg font-semibold text-foreground">Usage Analytics</h3>
            <p className="text-xs md:text-sm text-muted-foreground">Daily playback metrics</p>
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => onChartTypeChange('line')}
            className={`px-3 py-2 rounded-lg text-xs font-medium transition-all ${
              chartType === 'line' ?'bg-primary text-primary-foreground' :'bg-muted text-muted-foreground hover:bg-muted/80'
            }`}
          >
            <Icon name="TrendingUp" size={16} className="inline mr-1" />
            Line
          </button>
          <button
            onClick={() => onChartTypeChange('bar')}
            className={`px-3 py-2 rounded-lg text-xs font-medium transition-all ${
              chartType === 'bar' ?'bg-primary text-primary-foreground' :'bg-muted text-muted-foreground hover:bg-muted/80'
            }`}
          >
            <Icon name="BarChart2" size={16} className="inline mr-1" />
            Bar
          </button>
        </div>
      </div>

      {isLoading ? (
        <div className="w-full h-64 md:h-80 flex items-center justify-center">
          <div className="text-center">
            <Icon name="Loader2" size={32} className="animate-spin text-primary mx-auto mb-2" />
            <p className="text-sm text-muted-foreground">Loading usage data...</p>
          </div>
        </div>
      ) : data?.length === 0 ? (
        <div className="w-full h-64 md:h-80 flex items-center justify-center">
          <div className="text-center">
            <Icon name="BarChart3" size={32} className="text-muted-foreground mx-auto mb-2" />
            <p className="text-sm text-muted-foreground">No usage data available</p>
          </div>
        </div>
      ) : (
      <div className="w-full h-64 md:h-80" aria-label="Usage Analytics Chart">
        <ResponsiveContainer width="100%" height="100%">
          {chartType === 'line' ? (
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
              <XAxis 
                dataKey="date" 
                stroke="var(--color-muted-foreground)"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="var(--color-muted-foreground)"
                style={{ fontSize: '12px' }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend 
                wrapperStyle={{ fontSize: '12px' }}
                iconType="circle"
              />
              <Line 
                type="monotone" 
                dataKey="hoursWatched" 
                name="Hours Watched"
                stroke="var(--color-primary)" 
                strokeWidth={2}
                dot={{ fill: 'var(--color-primary)', r: 4 }}
                activeDot={{ r: 6 }}
              />
              <Line 
                type="monotone" 
                dataKey="totalPlays" 
                name="Total Plays"
                stroke="var(--color-secondary)" 
                strokeWidth={2}
                dot={{ fill: 'var(--color-secondary)', r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          ) : (
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
              <XAxis 
                dataKey="date" 
                stroke="var(--color-muted-foreground)"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="var(--color-muted-foreground)"
                style={{ fontSize: '12px' }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend 
                wrapperStyle={{ fontSize: '12px' }}
                iconType="circle"
              />
              <Bar 
                dataKey="hoursWatched" 
                name="Hours Watched"
                fill="var(--color-primary)" 
                radius={[4, 4, 0, 0]}
              />
              <Bar 
                dataKey="totalPlays" 
                name="Total Plays"
                fill="var(--color-secondary)" 
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
      )}
    </div>
  );
};

export default UsageChart;