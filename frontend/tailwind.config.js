/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        border: 'var(--color-border)', // slate-700
        input: 'var(--color-input)', // slate-700
        ring: 'var(--color-ring)', // blue-500
        background: 'var(--color-background)', // slate-900
        foreground: 'var(--color-foreground)', // slate-100
        primary: {
          DEFAULT: 'var(--color-primary)', // blue-500
          foreground: 'var(--color-primary-foreground)', // white
        },
        secondary: {
          DEFAULT: 'var(--color-secondary)', // indigo-500
          foreground: 'var(--color-secondary-foreground)', // white
        },
        destructive: {
          DEFAULT: 'var(--color-destructive)', // red-500
          foreground: 'var(--color-destructive-foreground)', // white
        },
        muted: {
          DEFAULT: 'var(--color-muted)', // slate-700
          foreground: 'var(--color-muted-foreground)', // slate-400
        },
        accent: {
          DEFAULT: 'var(--color-accent)', // amber-500
          foreground: 'var(--color-accent-foreground)', // black
        },
        popover: {
          DEFAULT: 'var(--color-popover)', // slate-800
          foreground: 'var(--color-popover-foreground)', // slate-100
        },
        card: {
          DEFAULT: 'var(--color-card)', // slate-800
          foreground: 'var(--color-card-foreground)', // slate-100
        },
        success: {
          DEFAULT: 'var(--color-success)', // emerald-500
          foreground: 'var(--color-success-foreground)', // white
        },
        warning: {
          DEFAULT: 'var(--color-warning)', // amber-500
          foreground: 'var(--color-warning-foreground)', // black
        },
        error: {
          DEFAULT: 'var(--color-error)', // red-500
          foreground: 'var(--color-error-foreground)', // white
        },
      },
      borderRadius: {
        sm: 'var(--radius-sm)', // 6px
        md: 'var(--radius-md)', // 10px
        lg: 'var(--radius-lg)', // 14px
        xl: 'var(--radius-xl)', // 18px
      },
      fontFamily: {
        heading: ['JetBrains Mono', 'monospace'],
        body: ['Inter', 'sans-serif'],
        caption: ['Source Sans 3', 'sans-serif'],
        data: ['SF Mono', 'Courier New', 'monospace'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      transitionDuration: {
        '250': '250ms',
      },
      transitionTimingFunction: {
        'smooth': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
      boxShadow: {
        'elevation-1': '0 1px 3px rgba(0, 0, 0, 0.3)',
        'elevation-2': '0 2px 8px rgba(0, 0, 0, 0.3)',
        'elevation-3': '0 6px 16px rgba(0, 0, 0, 0.3)',
        'elevation-4': '0 12px 24px rgba(0, 0, 0, 0.3)',
        'elevation-5': '0 20px 40px -8px rgba(0, 0, 0, 0.3)',
      },
      keyframes: {
        pulse: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        },
      },
      animation: {
        'pulse-subtle': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('tailwindcss-animate'),
  ],
}