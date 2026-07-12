import React from 'react';
import {Bg, Eyebrow, Words, useEnter, Spacer} from '../lib/anim';
import {C, disp} from '../theme';

const Row: React.FC<{delay: number; method: string; give: string; lead?: boolean}> = ({delay, method, give, lead}) => {
  const e = useEnter(delay, 24);
  return (
    <div style={{...e, display: 'grid', gridTemplateColumns: '1fr 60px 1.15fr', alignItems: 'center', gap: 34,
      padding: lead ? '26px 0 2px' : '18px 0'}}>
      <div style={{fontFamily: disp, fontWeight: 600, fontSize: lead ? 46 : 37,
        color: lead ? C.ink : C.mut, textAlign: 'right', letterSpacing: '-0.01em'}}>{method}</div>
      <div style={{fontSize: 36, color: lead ? C.amber : '#5f716c', textAlign: 'center'}}>→</div>
      <div style={{fontSize: lead ? 40 : 34, color: lead ? C.body : C.mut, fontWeight: lead ? 600 : 400}}>{give}</div>
    </div>
  );
};

// The "how we're stronger vs traditional" beat.
export const VsTraditional: React.FC = () => {
  const rule = useEnter(70, 0);
  return (
    <Bg>
      <Eyebrow>Why it's different · vs the usual playbook</Eyebrow>
      <Spacer f={0.5} />
      <Words size={66} delay={8} maxWidth={1400} parts={[{t: 'Same data. '}, {t: 'A sharper question.', color: C.amber}]} />
      <div style={{marginTop: 44}}>
        <Row delay={28} method="Differential expression" give="an association, not a cause" />
        <Row delay={44} method="Human genetics" give="a locus, not always a direction" />
        <Row delay={60} method="Bulk CRISPR screens" give="one fitness readout, no cell state" />
        <div style={{...rule, height: 1, background: C.line, margin: '16px 0'}} />
        <Row delay={80} method="Brakepoint" give="a causal effect — with its sign" lead />
      </div>
      <Spacer />
    </Bg>
  );
};
