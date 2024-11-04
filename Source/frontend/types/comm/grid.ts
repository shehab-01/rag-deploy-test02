import type { GridSettings } from 'handsontable/settings';

/**
 * Base table settings that will cascade to columns and cells.
 */
export interface GridDefSettings extends GridSettings {
  stretchH?: 'none' | 'all' | 'last' | any;
  page?: number;
  pagination?: boolean;
}
