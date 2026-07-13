import React from 'react';
import {Bg, Eyebrow, Words, useEnter, Spacer} from '../lib/anim';
import {C, disp} from '../theme';

const GENES = ['CBLB', 'CD5', 'DGKA', 'SMAD3', 'UBASH3A'];

export const Close: React.FC = () => {
  const pills = useEnter(26, 22);
  const code = useEnter(38, 26);
  const cta = useEnter(52, 20);
  const foot = useEnter(64, 18);
  return (
    <Bg>
      <Eyebrow>The result · open source (MIT)</Eyebrow>
      <Spacer />
      <Words size={86} delay={10} maxWidth={1320}
        parts={[{t: 'Five candidate brakes. Lead: '}, {t: 'CBLB', color: C.amber}, {t: '.'}]} />
      <div style={{...pills, display: 'flex', gap: 14, marginTop: 30, flexWrap: 'wrap'}}>
        {GENES.map((g) => (
          <div key={g} style={{
            fontFamily: disp, fontWeight: 600, fontSize: 26, letterSpacing: '0.01em',
            color: g === 'CBLB' ? '#0a1211' : C.body,
            background: g === 'CBLB' ? C.amber : 'rgba(255,255,255,0.05)',
            border: `1px solid ${g === 'CBLB' ? C.amber : C.line}`, borderRadius: 999, padding: '10px 26px'}}>{g}</div>
        ))}
      </div>
      <div style={{...code, fontFamily: 'ui-monospace, monospace', whiteSpace: 'pre', fontSize: 30, lineHeight: 1.85, background: '#0c1614', border: `1px solid ${C.line}`, borderRadius: 20, padding: '30px 40px', maxWidth: 620, marginTop: 34, color: '#d6e6e1'}}>
        <span style={{color: '#6f8f88'}}># every number, from a clean clone</span>{'\n'}make smoke{'\n'}make figure
      </div>
      <div style={{...cta, fontSize: 27, color: C.mut, marginTop: 26, maxWidth: 1150, lineHeight: 1.4}}>
        Explore the live map · clone the repo · help find the brakes today's drugs still miss.
      </div>
      <Spacer />
      <div style={{...foot, display: 'flex', alignItems: 'center', gap: 14, fontFamily: disp, fontSize: 26, color: C.ink, fontWeight: 600}}>
        <div style={{width: 24, height: 24, borderRadius: 7, background: 'conic-gradient(from 210deg, #0d9488, #d97a12)'}} />
        Brakepoint · Built with Claude Science.
      </div>
    </Bg>
  );
};
