import React from 'react';
import {Bg, Eyebrow, Words, useEnter, Spacer} from '../lib/anim';
import {C} from '../theme';
export const Title: React.FC = () => {
  const sub = useEnter(26, 26); const foot = useEnter(40, 20);
  return (
    <Bg>
      <Eyebrow>Built with Claude · Life Sciences · Research track</Eyebrow>
      <Spacer />
      <Words size={112} delay={10} maxWidth={1320}
        parts={[{t: "A T cell's "}, {t: 'brakes', color: C.amber}, {t: ' are its best drug targets.'}]} />
      <div style={{...sub, fontSize: 40, color: C.mut, marginTop: 38, maxWidth: 1250, lineHeight: 1.4}}>
        Druggable-brake target discovery from a 2.6-million-cell CRISPRi screen — built with Claude Science.
      </div>
      <Spacer />
      <div style={{...foot, display: 'flex', alignItems: 'center', gap: 16, fontSize: 23, color: C.mut}}>
        <div style={{width: 26, height: 26, borderRadius: 8, background: 'conic-gradient(from 210deg, #0d9488, #d97a12)'}} />
        Gladstone genome-scale CD4⁺ T-cell CRISPRi Perturb-seq · Marson lab
      </div>
    </Bg>
  );
};
