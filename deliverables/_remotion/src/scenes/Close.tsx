import React from 'react';
import {Bg, Eyebrow, Words, useEnter, Spacer} from '../lib/anim';
import {C, disp} from '../theme';
export const Close: React.FC = () => {
  const code = useEnter(30, 26);
  const foot = useEnter(50, 20);
  return (
    <Bg>
      <Eyebrow>Reproducible by design</Eyebrow>
      <Spacer />
      <Words size={88} delay={10} maxWidth={1500} parts={[{t: 'One command. '}, {t: 'Fixed seeds.', color: C.teal}, {t: ' MIT.'}]} />
      <div style={{...code, fontFamily: 'ui-monospace, monospace', whiteSpace: 'pre', fontSize: 34, lineHeight: 1.9, background: '#0c1614', border: `1px solid ${C.line}`, borderRadius: 22, padding: '44px 48px', maxWidth: 640, marginTop: 44, color: '#d6e6e1'}}>
        <span style={{color: '#6f8f88'}}># runs anywhere</span>{'\n'}
        <span style={{color: C.teal}}>make smoke</span>{'\n'}
        <span style={{color: C.teal}}>make figure</span>
      </div>
      <Spacer />
      <div style={{...foot, fontFamily: disp, fontSize: 27, color: C.ink, fontWeight: 600}}>Brakepoint · Built with Claude Science.</div>
    </Bg>
  );
};
