import React from 'react';
import {FigureScene} from './FigureScene';
import {C} from '../theme';
export const Brakes: React.FC = () => (
  <FigureScene eyebrow="Reported honestly"
    title={[{t: 'CD5 and DGKA '}, {t: 'hold up', color: C.amber}, {t: ' across donors.'}]}
    img="donor_consistency.png"
    caption="CBLB, SMAD3 and UBASH3A are donor-split at n=2 — a prioritized shortlist for the full cohort, not a finished target list." />
);
