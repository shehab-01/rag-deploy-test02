import type { ThemeTypes } from '@/types/themeTypes/ThemeType';

type AddThemeTypes = {
  colors: {
    valid: string;
    red: string;
    dark: string;
    gray: string;
  };
};
type CustomThemeTypes = ThemeTypes & AddThemeTypes;

const PurpleTheme: CustomThemeTypes = {
  name: 'PurpleTheme',
  dark: false,
  variables: {
    // 'border-color': '#eeeeee',
    'border-color': '#000000',
    'carousel-control-size': 10
  },
  colors: {
    primary: '#5D87FF',
    secondary: '#49BEFF',
    info: '#539BFF',
    success: '#13DEB9',
    accent: '#FFAB91',
    warning: '#FFAE1F',
    error: '#ED143D',
    muted: '#5a6a85',
    lightprimary: '#ECF2FF',
    lightsecondary: '#E8F7FF',
    lightsuccess: '#E6FFFA',
    lighterror: '#FDEDE8',
    lightwarning: '#FEF5E5',
    textPrimary: '#2A3547',
    textSecondary: '#2A3547',
    borderColor: '#e5eaef',
    inputBorder: '#000',
    containerBg: '#ffffff',
    hoverColor: '#f6f9fc',
    surface: '#fff',
    'on-surface-variant': '#fff',
    valid: '#FA896B',
    red: '#ED143D',
    dark: '#424242',
    gray: '#F0F0F0',
    grey100: '#F2F6FA',
    grey200: '#EAEFF4'
  }
};

// ADD:
const BlueTheme: ThemeTypes = {
  name: 'BlueTheme',
  dark: false,
  variables: {
    'border-color': '#e5eaef'
  },
  colors: {
    primary: '#186dde',
    secondary: '#0acc95',
    info: '#7460ee',
    success: '#13DEB9',
    accent: '#fc4b6c',
    warning: '#fec90f',
    error: '#ef5350',
    lightprimary: '#f5fcfd',
    lightsecondary: '#E8F7FF',
    lightsuccess: '#E6FFFA',
    lighterror: '#FDEDE8',
    lightwarning: '#FEF5E5',
    lightinfo: '#EBF3FE',
    textPrimary: '#2A3547',
    textSecondary: '#2A3547',
    borderColor: '#e5eaef',
    inputBorder: '#DFE5EF',
    containerBg: '#ffffff',
    // background: '#f4f6f9',
    hoverColor: '#f6f9fc',
    surface: '#fff',
    'on-surface-variant': '#fff',
    grey100: '#F2F6FA',
    grey200: '#EAEFF4',
    muted: '#1d2228'
    // borderline: '#1d1d1d'
  }
};

export { PurpleTheme, BlueTheme };
