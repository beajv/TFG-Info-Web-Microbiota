/**
 * @file chartjs-boxplot.d.ts
 * @description
 * Este archivo declara módulos personalizados para permitir que TypeScript reconozca correctamente
 * el paquete `chartjs-chart-box-and-violin-plot`, que extiende Chart.js con gráficos tipo boxplot y violin.
 * 
 * Contiene:
 * - La declaración general del módulo.
 * - Exportaciones específicas para `BoxPlotController` y `BoxAndWhiskers` que se utilizan en gráficos boxplot.
 */
declare module 'chartjs-chart-box-and-violin-plot';
declare module 'chartjs-chart-box-and-violin-plot/build/Chart.BoxPlot.js' {
    import { ChartComponentLike } from 'chart.js';
    const BoxPlotController: ChartComponentLike;
    const BoxAndWhiskers: ChartComponentLike;
    export { BoxPlotController, BoxAndWhiskers };
  }