import React from 'react';
import {Bg, Eyebrow, Words, Bullet, Spacer} from '../lib/anim';
import {C} from '../theme';
export const Brakes: React.FC = () => (
  <Bg>
    <Eyebrow>The therapeutic quadrant</Eyebrow>
    <Spacer f={0.5} />
    <Words size={64} delay={10} maxWidth={1420} parts={[{t: 'The positive quadrant — '}, {t: 'reported honestly.', color: C.amber}]} />
    <div style={{display: 'flex', flexDirection: 'column', gap: 32, marginTop: 44, maxWidth: 1560}}>
      <Bullet color={C.amber} delay={34}>Known brakes <b style={{color: C.ink}}>CD5, DGKA</b> land here and are donor-consistent — a consistency check.</Bullet>
      <Bullet color={C.teal} delay={64}>But at two donors the quadrant is <b style={{color: C.ink}}>not yet enriched</b> for a known-brake set (Mann–Whitney p = 0.56); its strongest raw hits include likely artifacts.</Bullet>
      <Bullet color={C.teal} delay={94}>So the positive side is an honest, prioritized <b style={{color: C.ink}}>hypothesis space</b> for the full four-donor cohort — the validated result is the machinery axis.</Bullet>
    </div>
    <Spacer />
  </Bg>
);
