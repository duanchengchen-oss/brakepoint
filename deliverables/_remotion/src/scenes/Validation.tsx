import React from 'react';
import {Bg, Eyebrow, Bullet, useEnter, Spacer} from '../lib/anim';
import {C, disp} from '../theme';
export const Validation: React.FC = () => {
  const name = useEnter(10, 26);
  return (
    <Bg>
      <Eyebrow>The lead · CBLB</Eyebrow>
      <Spacer f={0.4} />
      <div style={{display: 'flex', alignItems: 'center', gap: 70}}>
        <div style={{...name, flex: 'none'}}>
          <div style={{fontFamily: disp, fontWeight: 700, fontSize: 150, color: '#fff', letterSpacing: '-0.03em', lineHeight: 1}}>CBLB</div>
          <div style={{fontSize: 26, color: C.amber, marginTop: 10, fontWeight: 600}}>inhibitors already in early-phase trials</div>
        </div>
        <div style={{display: 'flex', flexDirection: 'column', gap: 26, maxWidth: 940}}>
          <Bullet color={C.amber} delay={40}>Two oral CBL-B inhibitors already in trials — <b style={{color: C.ink}}>NX-1607 (Ph1), HST-1011 (Ph1/2)</b>.</Bullet>
          <Bullet color={C.teal} delay={70}>An <b style={{color: C.ink}}>autoimmune genetic association</b> — loss-of-function consistent with a brake, so inhibiting it may boost immunity.</Bullet>
          <Bullet color={C.teal} delay={100}>Top-decile causal effect in the brake quadrant. <b style={{color: C.ink}}>CD5</b> and <b style={{color: C.ink}}>DGKA</b> follow — donor-consistent, with external tractability evidence.</Bullet>
        </div>
      </div>
      <Spacer />
    </Bg>
  );
};
