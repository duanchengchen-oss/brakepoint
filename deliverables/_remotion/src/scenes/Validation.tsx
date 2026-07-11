import React from 'react';
import {Bg, Eyebrow, Words, CountUp, useEnter, Spacer} from '../lib/anim';
import {C, disp} from '../theme';
export const Validation: React.FC = () => {
  const para = useEnter(40, 26);
  return (
    <Bg>
      <Eyebrow>Validation · it recovers ground truth</Eyebrow>
      <Spacer />
      <div style={{display: 'flex', alignItems: 'center', gap: 80}}>
        <div style={{flex: 'none', textAlign: 'center'}}>
          <div style={{fontFamily: disp, fontWeight: 700, fontSize: 150, color: '#fff', lineHeight: 1, letterSpacing: '-0.03em'}}>
            <CountUp to={14} dur={40} /><span style={{fontSize: 80, color: C.mut}}>/15</span>
          </div>
          <div style={{fontSize: 26, color: C.mut, marginTop: 14, maxWidth: 260, marginInline: 'auto'}}>largest effects are machinery, not targets</div>
        </div>
        <div>
          <Words size={62} delay={10} maxWidth={780} parts={[{t: 'Unsupervised, the biggest effects are the '}, {t: 'TCR module.', color: C.teal}]} />
          <div style={{...para, fontSize: 34, color: C.body, marginTop: 28, maxWidth: 800, lineHeight: 1.4}}>ZAP70, the CD3 complex, LAT — and the direction axis flags every one as machinery, <b style={{color: C.ink}}>donor-consistently</b>. That machinery result is the load-bearing one.</div>
        </div>
      </div>
      <Spacer />
    </Bg>
  );
};
