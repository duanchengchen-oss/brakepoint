import React from 'react';
import {Bg, Eyebrow, Words, useEnter, Spacer} from '../lib/anim';
import {C, disp} from '../theme';

export const Title: React.FC = () => {
  const sub = useEnter(26, 26);
  const foot = useEnter(40, 20);
  return (
    <Bg>
      <Eyebrow>Built with Claude · Life Sciences · Research track</Eyebrow>
      <Spacer />
      <Words size={116} delay={10} maxWidth={1250}
        parts={[{t: 'A signed causal map of '}, {t: 'T-cell function.', color: C.amber}]} />
      <div style={{...sub, fontSize: 42, color: C.mut, marginTop: 40, maxWidth: 1200, lineHeight: 1.4}}>
        Drug-target discovery from a 2.64-million-cell CRISPRi Perturb-seq screen — built end-to-end with Claude Science.
      </div>
      <Spacer />
      <div style={{...foot, display: 'flex', alignItems: 'center', gap: 16, fontSize: 23, color: C.mut}}>
        <div style={{width: 26, height: 26, borderRadius: 8, background: 'conic-gradient(from 210deg, #0d9488, #d97a12)'}} />
        Gladstone genome-scale CD4⁺ T-cell Perturb-seq · Marson lab
      </div>
    </Bg>
  );
};
