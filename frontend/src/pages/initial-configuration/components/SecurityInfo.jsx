import React from 'react';
import Icon from '../../../components/AppIcon';

const SecurityInfo = () => {
  const securityFeatures = [
    {
      icon: 'Lock',
      title: 'Encrypted Storage',
      description: 'All API keys are encrypted using AES-256 before being stored locally'
    },
    {
      icon: 'Shield',
      title: 'Secure Transmission',
      description: 'Connections use HTTPS/TLS protocols to prevent interception'
    },
    {
      icon: 'Eye',
      title: 'Privacy First',
      description: 'Your credentials never leave your local network or device'
    },
    {
      icon: 'RefreshCw',
      title: 'Easy Updates',
      description: 'Reconfigure services anytime without affecting existing data'
    }
  ];

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6 shadow-elevation-2">
      <div className="flex items-center gap-3 mb-4 md:mb-6">
        <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-primary/10">
          <Icon name="ShieldCheck" size={20} color="var(--color-primary)" />
        </div>
        <div>
          <h3 className="text-base md:text-lg font-semibold text-foreground">Security & Privacy</h3>
          <p className="text-xs md:text-sm text-muted-foreground">Your data protection measures</p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4">
        {securityFeatures?.map((feature, index) => (
          <div 
            key={index}
            className="p-3 md:p-4 bg-muted/30 rounded-lg border border-border hover:border-primary/50 transition-all"
          >
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center bg-primary/10 flex-shrink-0">
                <Icon name={feature?.icon} size={16} color="var(--color-primary)" />
              </div>
              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-semibold text-foreground mb-1">{feature?.title}</h4>
                <p className="text-xs text-muted-foreground leading-relaxed">{feature?.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-4 md:mt-6 p-3 md:p-4 bg-accent/10 border border-accent/20 rounded-lg">
        <div className="flex items-start gap-3">
          <Icon name="Info" size={18} color="var(--color-accent)" className="flex-shrink-0 mt-0.5" />
          <div className="flex-1 min-w-0">
            <p className="text-xs md:text-sm text-foreground">
              <strong>Self-Hosted Security:</strong> This application runs entirely on your infrastructure. 
              No data is transmitted to external servers, ensuring complete privacy and control over your media server credentials.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SecurityInfo;