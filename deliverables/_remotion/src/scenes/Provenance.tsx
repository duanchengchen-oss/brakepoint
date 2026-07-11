import React from 'react';
import {Bg, Eyebrow, Words, Bullet, Spacer} from '../lib/anim';
import {C} from '../theme';
export const Provenance: React.FC = () => (
  <Bg>
    <Eyebrow>How Claude Science got us there</Eyebrow>
    <Spacer />
    <Words size={66} delay={10} maxWidth={1300} parts={[{t: 'Every number carries its '}, {t: 'provenance.', color: C.amber}]} />
    <div style={{display: 'flex', flexDirection: 'column', gap: 34, marginTop: 48, maxWidth: 1520}}>
      <Bullet color={C.teal} delay={34}>Each result is a <b style={{color: C.ink}}>versioned artifact</b> — its exact code, environment, and the conversation that produced it.</Bullet>
      <Bullet color={C.amber} delay={64}>A background <b style={{color: C.ink}}>reviewer</b> checks every claim against what actually ran — it caught a <b style={{color: C.ink}}>real statistical bug</b> before it reached a figure.</Bullet>
      <Bullet color={C.teal} delay={94}>Heavy compute runs on an <b style={{color: C.ink}}>NVIDIA DGX Spark</b>; the signed map over 2.6M cells finishes in <b style={{color: C.ink}}>~40 seconds</b>.</Bullet>
    </div>
    <Spacer />
  </Bg>
);
