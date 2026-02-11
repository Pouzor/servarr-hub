import React from 'react';
import Icon from '../../../components/AppIcon';

const UserStatsCard = ({ totalUsers, activeUsers, newUsers, growthRate }) => {
  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 md:w-12 md:h-12 rounded-lg bg-primary/10 flex items-center justify-center">
            <Icon name="Users" size={20} color="var(--color-primary)" />
          </div>
          <div>
            <h3 className="text-base md:text-lg font-semibold text-foreground">User Statistics</h3>
            <p className="text-xs md:text-sm text-muted-foreground">Total registered users</p>
          </div>
        </div>
        
        <div className={`flex items-center gap-1 px-2 py-1 rounded-md ${growthRate >= 0 ? 'bg-success/10 text-success' : 'bg-error/10 text-error'}`}>
          <Icon name={growthRate >= 0 ? 'TrendingUp' : 'TrendingDown'} size={14} />
          <span className="text-xs font-semibold">{Math.abs(growthRate)}%</span>
        </div>
      </div>
      <div className="space-y-4">
        <div>
          <div className="flex items-baseline gap-2 mb-1">
            <span className="text-3xl md:text-4xl font-bold text-foreground">{totalUsers}</span>
            <span className="text-sm text-muted-foreground">total users</span>
          </div>
          <div className="w-full bg-muted rounded-full h-2">
            <div 
              className="bg-primary rounded-full h-2 transition-all duration-500"
              style={{ width: `${(activeUsers / totalUsers) * 100}%` }}
            ></div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-muted/30 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <Icon name="Activity" size={16} color="var(--color-success)" />
              <span className="text-xs text-muted-foreground">Active Now</span>
            </div>
            <p className="text-xl md:text-2xl font-bold text-foreground">{activeUsers}</p>
          </div>

          <div className="bg-muted/30 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <Icon name="UserPlus" size={16} color="var(--color-accent)" />
              <span className="text-xs text-muted-foreground">New (30d)</span>
            </div>
            <p className="text-xl md:text-2xl font-bold text-foreground">{newUsers}</p>
          </div>
        </div>

        <div className="pt-3 border-t border-border">
          <div className="flex items-center justify-between text-xs md:text-sm">
            <span className="text-muted-foreground">Activity Rate</span>
            <span className="font-semibold text-foreground">{((activeUsers / totalUsers) * 100)?.toFixed(1)}%</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserStatsCard;