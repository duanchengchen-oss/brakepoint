import React from 'react';
import {Bg, Eyebrow, Words, CountUp, useEnter, Spacer} from '../lib/anim';
import {C, disp} from '../theme';
const Kpi: React.FC<{delay: number; num: React.ReactNode; label: string}> = ({delay, num, label}) => {
  const e = useEnter(delay, 30);
  return (
    <div style={{...e}}>
      <div style={{fontFamily: disp, fontSize: 72, fontWeight: 600, color: '#fff', letterSpacing: '-0.02em'}}>{num}</div>
      <div style={{fontSize: 24, color: C.mut, marginTop: 6, maxWidth: 290}}>{label}</div>
    </div>
  );
};
export const Provenance: React.FC = () => (
  <Bg>
    <Eyebrow>The screen</Eyebrow>
    <Spacer />
    <Words size={72} delay={10} maxWidth={1300} parts={[{t: 'A genome-scale '}, {t: 'CRISPRi screen', color: C.teal}, {t: '.'}]} />
    <Spacer />
    <div style={{display: 'flex', gap: 70}}>
      <Kpi delay={40} num={<CountUp to={2638736} delay={40} dur={46} />} label="primary human CD4⁺ T cells" />
      <Kpi delay={54} num={<CountUp to={12449} delay={54} dur={40} />} label="gene knockdowns" />
      <Kpi delay={68} num="Gladstone" label="Marson lab · 2 donors · Stim 8h" />
    </div>
  </Bg>
);
