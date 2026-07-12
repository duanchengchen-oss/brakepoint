import React from 'react';
import {FigureScene} from './FigureScene';
import {C} from '../theme';
export const Method: React.FC = () => (
  <FigureScene eyebrow="The finding · target shortlist"
    title={[{t: 'Five druggable brakes, ranked by '}, {t: 'convergent evidence', color: C.amber}, {t: '.'}]}
    img="target_matrix.png"
    caption="causal effect · direction · donor consistency · safety · druggability · immune genetics · clinical precedent" />
);
