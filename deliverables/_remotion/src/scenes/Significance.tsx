import React from 'react';
import {FigureScene} from './FigureScene';
import {C} from '../theme';

// The computational-novelty beat: significance saturates at scale, so rank by effect size.
export const Significance: React.FC = () => (
  <FigureScene
    eyebrow="The trap · significance"
    title={[{t: "Significance can't rank a "}, {t: 'million-cell screen', color: C.teal}, {t: '.'}]}
    img="significance_wall.png"
    caption="97.5% of tested knockdowns clear q<0.05 — so we rank by causal effect size, not p-value." />
);
