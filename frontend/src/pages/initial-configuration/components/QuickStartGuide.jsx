import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const QuickStartGuide = () => {
  const [expandedStep, setExpandedStep] = useState(null);

  const steps = [
    {
      id: 1,
      title: 'Locate Your API Keys',
      icon: 'Key',
      description: 'Find API keys in each service\'s settings',
      details: [
        'Radarr: Settings → General → Security → API Key',
        'Sonarr: Settings → General → Security → API Key',
        'Jellyfin: Dashboard → API Keys → Create New Key',
        'Jellyseerr: Settings → General → API Key'
      ]
    },
    {
      id: 2,
      title: 'Enter Service URLs',
      icon: 'Link',
      description: 'Provide the full URL for each service',
      details: [
        'Include protocol: http:// or https://',
        'Use local IP for same-network access: http://192.168.1.100',
        'Use domain for remote access: https://radarr.yourdomain.com',
        'Port numbers are optional if using standard ports'
      ]
    },
    {
      id: 3,
      title: 'Test Connections',
      icon: 'Zap',
      description: 'Verify each service connection works',
      details: [
        'Click "Test Connection" for each service',
        'Green checkmark indicates successful connection',
        'Red X shows connection failure with error details',
        'Fix any errors before proceeding to save'
      ]
    },
    {
      id: 4,
      title: 'Save Configuration',
      icon: 'Save',
      description: 'Store your settings securely',
      details: [
        'All services must show successful connection',
        'Click "Save All Configurations" at the bottom',
        'Credentials are encrypted before storage',
        'You can reconfigure anytime from this screen'
      ]
    }
  ];

  const toggleStep = (stepId) => {
    setExpandedStep(expandedStep === stepId ? null : stepId);
  };

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6 shadow-elevation-2">
      <div className="flex items-center gap-3 mb-4 md:mb-6">
        <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-secondary/10">
          <Icon name="BookOpen" size={20} color="var(--color-secondary)" />
        </div>
        <div>
          <h3 className="text-base md:text-lg font-semibold text-foreground">Quick Start Guide</h3>
          <p className="text-xs md:text-sm text-muted-foreground">Follow these steps to configure your services</p>
        </div>
      </div>
      <div className="space-y-3">
        {steps?.map((step, index) => (
          <div 
            key={step?.id}
            className="border border-border rounded-lg overflow-hidden transition-all hover:border-primary/50"
          >
            <button
              onClick={() => toggleStep(step?.id)}
              className="w-full p-3 md:p-4 flex items-center justify-between bg-muted/30 hover:bg-muted/50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center bg-primary/10 flex-shrink-0">
                  <Icon name={step?.icon} size={16} color="var(--color-primary)" />
                </div>
                <div className="text-left">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-primary">Step {index + 1}</span>
                    <h4 className="text-sm font-semibold text-foreground">{step?.title}</h4>
                  </div>
                  <p className="text-xs text-muted-foreground mt-0.5">{step?.description}</p>
                </div>
              </div>
              <Icon 
                name={expandedStep === step?.id ? 'ChevronUp' : 'ChevronDown'} 
                size={18} 
                className="text-muted-foreground flex-shrink-0"
              />
            </button>

            {expandedStep === step?.id && (
              <div className="p-3 md:p-4 bg-background border-t border-border">
                <ul className="space-y-2">
                  {step?.details?.map((detail, detailIndex) => (
                    <li key={detailIndex} className="flex items-start gap-2 text-xs md:text-sm text-muted-foreground">
                      <Icon name="Check" size={14} className="text-success flex-shrink-0 mt-0.5" />
                      <span>{detail}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="mt-4 md:mt-6 p-3 md:p-4 bg-primary/10 border border-primary/20 rounded-lg">
        <div className="flex items-start gap-3">
          <Icon name="Lightbulb" size={18} color="var(--color-primary)" className="flex-shrink-0 mt-0.5" />
          <div className="flex-1 min-w-0">
            <p className="text-xs md:text-sm text-foreground mb-2">
              <strong>Pro Tip:</strong> Test each service individually before saving. This helps identify configuration issues early.
            </p>
            <Button
              variant="link"
              size="sm"
              iconName="ExternalLink"
              iconPosition="right"
              className="p-0 h-auto text-primary hover:text-primary/80"
            >
              View detailed documentation
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuickStartGuide;