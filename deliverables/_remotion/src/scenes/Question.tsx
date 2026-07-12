import React from 'react';
import {Bg, Eyebrow, Words, useEnter, Spacer} from '../lib/anim';
import {C} from '../theme';
export const Question: React.FC = () => {
  const sub = useEnter(70, 26);
  return (
    <Bg>
      <Eyebrow>The thesis</Eyebrow>
      <Spacer />
      <Words size={82} delay={10} maxWidth={1560}
        parts={[{t: 'Which knockdowns make a T‑cell a '}, {t: 'stronger', color: C.amber}, {t: ' effector?'}]} />
      <div style={{...sub, fontSize: 38, color: C.mut, marginTop: 36, maxWidth: 1300, lineHeight: 1.42}}>
        Checkpoint blockade and CAR-T both work by <b style={{color: C.body}}>releasing brakes</b> on T cells. We look for the druggable ones — genome-wide.
      </div>
      <Spacer />
    </Bg>
  );
};
