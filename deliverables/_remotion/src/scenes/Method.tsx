import React from 'react';
import {FigureScene} from './FigureScene';
import {C} from '../theme';
export const Method: React.FC = () => (
  <FigureScene eyebrow="The finding · target shortlist"
    title={[{t: 'Five candidate brakes, ranked by '}, {t: 'convergent evidence', color: C.amber}, {t: '.'}]}
    img="target_matrix.png"
    caption="causal effect · direction · donor consistency · viability · druggability · immune genetics · clinical precedent" />
);
