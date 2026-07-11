import React from 'react';
import {useCurrentFrame, useVideoConfig, spring} from 'remotion';
import {Bg, Eyebrow, Words, useEnter, Spacer} from '../lib/anim';
import {C, disp} from '../theme';
const Card: React.FC<{delay: number; from: number; grad: string; title: string; tcolor: string; children: React.ReactNode}> = ({delay, from, grad, title, tcolor, children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - delay, fps, config: {damping: 200}});
  return (
    <div style={{flex: 1, opacity: s, transform: `translateX(${(1 - s) * from}px)`, background: grad, border: `1px solid ${C.line}`, borderRadius: 26, padding: '44px 46px'}}>
      <div style={{fontFamily: disp, fontWeight: 600, fontSize: 40, color: tcolor}}>{title}</div>
      <div style={{fontSize: 29, lineHeight: 1.4, color: C.body, marginTop: 16}}>{children}</div>
    </div>
  );
};
export const Method: React.FC = () => {
  const sub = useEnter(84, 26);
  return (
    <Bg>
      <Eyebrow>The method · two axes</Eyebrow>
      <Spacer f={0.5} />
      <Words size={60} delay={10} maxWidth={1520} parts={[{t: 'Magnitude tells you '}, {t: 'how much.', color: C.teal}, {t: ' Only the sign tells you '}, {t: 'which way.', color: C.amber}]} />
      <div style={{display: 'flex', gap: 40, marginTop: 44}}>
        <Card delay={44} from={-30} grad="linear-gradient(180deg,rgba(13,148,136,0.16),rgba(13,148,136,0.03))" title="↓ direction < 0 — machinery" tcolor={C.teal}>Knockdown pushes cells <b style={{color: C.ink}}>away</b> from the effector program — required, not druggable.</Card>
        <Card delay={58} from={30} grad="linear-gradient(180deg,rgba(217,122,18,0.16),rgba(217,122,18,0.03))" title="↑ direction > 0 — a brake" tcolor={C.amber}>Knockdown pushes cells <b style={{color: C.ink}}>toward</b> the effector program — the therapeutic quadrant.</Card>
      </div>
      <div style={{...sub, fontSize: 31, color: C.mut, marginTop: 34, maxWidth: 1560}}>Axis 1 — power-equalized <b style={{color: C.body}}>energy distance</b> (causal magnitude). Axis 2 — a per-cell <b style={{color: C.body}}>effector minus dysfunction</b> score, over all 2.64 M cells.</div>
      <Spacer />
    </Bg>
  );
};
