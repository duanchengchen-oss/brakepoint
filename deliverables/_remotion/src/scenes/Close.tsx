import React from 'react';
import {Bg, Eyebrow, Words, useEnter, Spacer} from '../lib/anim';
import {C, disp} from '../theme';
export const Close: React.FC = () => {
  const code = useEnter(30, 26); const foot = useEnter(50, 20);
  return (
    <Bg>
      <Eyebrow>Open source · MIT</Eyebrow>
      <Spacer />
      <Words size={82} delay={10} maxWidth={1300} parts={[{t: 'Every target traces back to '}, {t: 'code', color: C.teal}, {t: '.'}]} />
      <div style={{...code, fontFamily: 'ui-monospace, monospace', whiteSpace: 'pre', fontSize: 34, lineHeight: 1.9, background: '#0c1614', border: `1px solid ${C.line}`, borderRadius: 22, padding: '40px 48px', maxWidth: 660, marginTop: 44, color: '#d6e6e1'}}>
        <span style={{color: '#6f8f88'}}># one command, from a clean clone</span>{'\n'}make smoke{'\n'}make figure
      </div>
      <Spacer />
      <div style={{...foot, fontFamily: disp, fontSize: 27, color: C.ink, fontWeight: 600}}>Brakepoint · Built with Claude Science.</div>
    </Bg>
  );
};
