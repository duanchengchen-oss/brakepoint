import React from 'react';
import {Bg, Eyebrow, Words, CountUp, useEnter, Spacer} from '../lib/anim';
import {C, disp} from '../theme';
const Kpi: React.FC<{delay: number; num: React.ReactNode; label: string}> = ({delay, num, label}) => {
  const e = useEnter(delay, 30);
  return (
    <div style={{...e, width: 350}}>
      <div style={{fontFamily: disp, fontSize: 74, fontWeight: 600, color: '#fff', letterSpacing: '-0.02em'}}>{num}</div>
      <div style={{fontSize: 24, color: C.mut, marginTop: 6, maxWidth: 280}}>{label}</div>
    </div>
  );
};
export const Question: React.FC = () => (
  <Bg>
    <Eyebrow>The question</Eyebrow>
    <Spacer />
    <Words size={82} delay={10} maxWidth={1640}
      parts={[{t: 'Which knockdowns make a T‑cell a '}, {t: 'better', color: C.amber},
        {t: ' effector — and which just '}, {t: 'break', color: C.teal}, {t: ' it?'}]} />
    <Spacer />
    <div style={{display: 'flex', gap: 70}}>
      <Kpi delay={64} num={<CountUp to={2638736} delay={64} dur={46} />} label="primary human CD4⁺ T cells" />
      <Kpi delay={78} num={<CountUp to={12449} delay={78} dur={40} />} label="CRISPRi knockdowns" />
      <Kpi delay={92} num="2 donors" label="scVI-integrated · Stim 8h" />
    </div>
  </Bg>
);
