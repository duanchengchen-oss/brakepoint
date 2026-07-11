import durations from '../public/durations.json';
export const DUR = durations as number[];
export const TR = 18; // crossfade frames
export const TOTAL = DUR.reduce((a, b) => a + b, 0) - TR * (DUR.length - 1);
