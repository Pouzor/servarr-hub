import React from 'react';
import Icon from '../../../components/AppIcon';

const StatisticsCard = ({ title, value, subtitle, icon, trend, trendValue, color = 'primary', details }) => {
  const getColorClasses = () => {
    const colors = {
      primary: 'bg-primary/10 text-primary border-primary/20',
      secondary: 'bg-secondary/10 text-secondary border-secondary/20',
      success: 'bg-success/10 text-success border-success/20',
      warning: 'bg-warning/10 text-warning border-warning/20',
      accent: 'bg-accent/10 text-accent border-accent/20'
    };
    return colors?.[color] || colors?.primary;
  };

  return (
    <div className="bg-card border border-border rounded-lg p-3 md:p-4 hover:shadow-elevation-2 transition-smooth">
      <div className="flex items-start gap-3 mb-3">
        <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${getColorClasses()}`}>
          <Icon name={icon} size={20} />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-xl md:text-2xl font-bold text-foreground mb-0.5 font-data">
            {value}
          </h3>
          <p className="text-xs text-muted-foreground">{title}</p>
          {subtitle && (
            <p className="text-xs text-muted-foreground/80 font-caption mt-0.5">{subtitle}</p>
          )}
        </div>
      </div>
      {details && details?.length > 0 && (
        <div className="mt-2 pt-2 border-t border-border/50 space-y-1">
          {details?.map((detail, index) => (
            <div key={index} className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">{detail?.label}</span>
              <span className="font-medium text-foreground">{detail?.value}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default StatisticsCard;