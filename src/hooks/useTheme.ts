import { useState, useEffect } from 'react';

interface Theme {
  name: string;
  bgColor: string;
  mainColor: string;
  subColor: string;
  textColor: string;
  accentColor?: string;
}

const themes: Theme[] = [
  {
    name: "light",
    bgColor: "#ffffff",
    mainColor: "#2563eb",
    subColor: "#6b7280", 
    textColor: "#111827",
    accentColor: "#2563eb"
  },
  {
    name: "dark",
    bgColor: "#0A0A0A",
    mainColor: "#3B82F6",
    subColor: "#6B7280",
    textColor: "#F9FAFB",
    accentColor: "#3B82F6"
  },
  {
    name: "japan",
    bgColor: "#1f2937",
    mainColor: "#ef4444",
    subColor: "#b91c1c",
    textColor: "#ffffff",
    accentColor: "#ef4444"
  },
  {
    name: "forest",
    bgColor: "#064e3b",
    mainColor: "#34d399",
    subColor: "#4ade80",
    textColor: "#ffffff",
    accentColor: "#34d399"
  },
  {
    name: "carbon",
    bgColor: "#1a1a1a",
    mainColor: "#f97316",
    subColor: "#fb923c",
    textColor: "#f5f5f5",
    accentColor: "#f97316"
  },
  {
    name: "geo",
    bgColor: "#1a1f36",
    mainColor: "#00d4ff",
    subColor: "#10b981",
    textColor: "#eef2ff",
    accentColor: "#00d4ff"
  },
  {
    name: "strawberry",
    bgColor: "#1f1013",
    mainColor: "#ff4d6d",
    subColor: "#c77c8a",
    textColor: "#fff0f3",
    accentColor: "#ff4d6d"
  },
  {
    name: "muted",
    bgColor: "#1f1f1f",
    mainColor: "#c5b4e3",
    subColor: "#6b7280",
    textColor: "#e2e8f0",
    accentColor: "#c5b4e3"
  },
  {
    name: "city night",
    bgColor: "#0f172a",
    mainColor: "#f5b1cc",
    subColor: "#64748b",
    textColor: "#e2e8f0",
    accentColor: "#f5b1cc"
  },
  {
    name: "dots",
    bgColor: "#ffffff",
    mainColor: "#dc2626",
    subColor: "#1e40af",
    textColor: "#dc2626",
    accentColor: "#dc2626"
  },
  {
    name: "brazil",
    bgColor: "#1e293b",
    mainColor: "#22c55e",
    subColor: "#fbbf24",
    textColor: "#f1f5f9",
    accentColor: "#22c55e"
  },
  {
    name: "ocean",
    bgColor: "#0c4a6e",
    mainColor: "#38bdf8",
    subColor: "#6b7280",
    textColor: "#f3f4f6",
    accentColor: "#38bdf8"
  },
  {
    name: "oblivion",
    bgColor: "#1e293b",
    mainColor: "#94a3b8",
    subColor: "#64748b",
    textColor: "#f1f5f9",
    accentColor: "#94a3b8"
  },
  {
    name: "nether",
    bgColor: "#881337",
    mainColor: "#fb7185",
    subColor: "#f43f5e",
    textColor: "#fecdd3",
    accentColor: "#fb7185"
  },
  {
    name: "skyscraper",
    bgColor: "#0f172a",
    mainColor: "#38bdf8",
    subColor: "#1e3a8a",
    textColor: "#f1f5f9",
    accentColor: "#38bdf8"
  },
  {
    name: "caldaia",
    bgColor: "#111111",
    mainColor: "#ff3333", // Main text and headers in bright red
    subColor: "#ff8533", // Subtitles and secondary text in bright orange
    textColor: "#ff3333", // Primary text in red to match headers
    accentColor: "#ffd700" // Gold accent for special elements
  }
];

export function useTheme(initialTheme: string = 'light') {
  const [activeTheme, setActiveTheme] = useState(initialTheme);
  const [isDark, setIsDark] = useState(false);

  const theme = themes.find(t => t.name === activeTheme) || themes[0];

  useEffect(() => {
    const root = document.documentElement;
    
    requestAnimationFrame(() => {
      root.style.setProperty('--theme-bg', theme.bgColor);
      root.style.setProperty('--theme-main', theme.mainColor);
      root.style.setProperty('--theme-sub', theme.subColor);
      root.style.setProperty('--theme-text', theme.textColor);
      root.style.setProperty('--theme-accent', theme.accentColor || theme.mainColor);
      
      // Set border color based on theme
      const borderColor = isDark 
        ? 'rgba(255, 255, 255, 0.1)' 
        : 'rgba(107, 114, 128, 0.1)';
      root.style.setProperty('--theme-border', borderColor);

      // Remove gradient background for caldaia theme
      if (theme.name === 'caldaia') {
        document.body.style.background = theme.bgColor;
      } else {
        document.body.style.background = '';
      }
    });
    
    setIsDark(theme.name === 'dark' || theme.bgColor.startsWith('#0') || theme.bgColor.startsWith('#1') || theme.bgColor.startsWith('#2'));
  }, [theme, isDark]);

  return {
    theme,
    themes,
    activeTheme,
    setActiveTheme,
    isDark,
    setIsDark
  };
}