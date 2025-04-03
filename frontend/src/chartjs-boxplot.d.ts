// src/chartjs-boxplot.d.ts
declare module 'chartjs-chart-box-and-violin-plot';
declare module 'chartjs-chart-box-and-violin-plot/build/Chart.BoxPlot.js' {
    import { ChartComponentLike } from 'chart.js';
    const BoxPlotController: ChartComponentLike;
    const BoxAndWhiskers: ChartComponentLike;
    export { BoxPlotController, BoxAndWhiskers };
  }