import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring} from 'remotion';
import {C, disp, sans} from '../theme';

// convergent-evidence matrix — rendered natively (dark) instead of embedding the figure.
// Causal-effect column = true e_distance percentiles among the 11,438 tested (data-fix).
const AXES = ['Causal\neffect', 'Brake\ndirection', 'Donor\nconsistency', 'Screen\nfitness', 'Target\ntractability', 'Immune\ngenetics', 'Clinical\nprecedent'];
type Row = {g: string; v: number[]; call: string; cc: 'amber' | 'teal' | 'slate'; note: string};
const ROWS: Row[] = [
  {g: 'CBLB', v: [0.96, 0.72, 0.35, 0.55, 1.00, 0.90, 0.90], call: 'LEAD', cc: 'amber', note: 'CBL-B inhibitors in trials · autoimmune association'},
  {g: 'CD5', v: [0.95, 0.75, 1.00, 0.90, 0.70, 0.50, 0.40], call: 'SCREEN-CONSISTENT', cc: 'teal', note: 'donor-consistent · CD5 deletion boosts CAR-T (preclinical)'},
  {g: 'DGKA', v: [0.78, 0.42, 1.00, 0.78, 1.00, 0.25, 0.85], call: 'SCREEN-CONSISTENT', cc: 'teal', note: 'donor-consistent · Bayer DGKα inhibitor Ph1'},
  {g: 'SMAD3', v: [1.00, 0.32, 0.35, 0.90, 0.60, 0.45, 0.55], call: 'EXPLORATORY', cc: 'slate', note: 'high-effect · TGF-β node · donor-split'},
  {g: 'UBASH3A', v: [0.69, 0.28, 0.35, 0.82, 0.55, 0.90, 0.15], call: 'GENETICS-LED', cc: 'slate', note: 'T1D/RA GWAS · tractable phosphatase · weak in screen'},
];
const CHIP = {amber: ['#f4b062', '#0a1211'], teal: ['rgba(47,214,191,0.16)', '#7fe9d8'], slate: ['rgba(255,255,255,0.06)', '#8fa39d']} as const;

const colX = (j: number) => 665 + j * 90;
const rowY = (i: number) => 410 + i * 108;
const lerp = (a: number, b: number, t: number) => Math.round(a + (b - a) * t);
const bubbleFill = (v: number) => `rgb(${lerp(70, 233, v)},${lerp(82, 243, v)},${lerp(78, 236, v)})`;

export const Method: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const titleS = spring({frame, fps, config: {damping: 200}});
  const headP = spring({frame: frame - 18, fps, config: {damping: 200}});

  return (
    <AbsoluteFill style={{backgroundColor: C.bg, fontFamily: sans}}>
      <AbsoluteFill style={{background:
        'radial-gradient(42% 50% at 14% 8%, rgba(13,148,136,0.18), transparent 60%),' +
        'radial-gradient(44% 50% at 90% 14%, rgba(217,122,18,0.16), transparent 62%)'}} />
      <div style={{position: 'absolute', top: 60, right: 130, fontFamily: disp, fontWeight: 600, letterSpacing: '0.3em', fontSize: 21, color: 'rgba(127,233,216,0.5)'}}>BRAKEPOINT</div>
      <div style={{position: 'absolute', top: 64, left: 130, opacity: titleS, transform: `translateY(${(1 - titleS) * 18}px)`}}>
        <div style={{display: 'inline-flex', alignItems: 'center', gap: 12, fontSize: 18, fontWeight: 700, letterSpacing: '0.26em', textTransform: 'uppercase', color: C.amber, background: 'rgba(244,176,98,0.09)', border: '1px solid rgba(244,176,98,0.22)', padding: '9px 18px', borderRadius: 999}}>The finding · target shortlist</div>
        <div style={{fontFamily: disp, fontWeight: 700, fontSize: 52, color: C.ink, marginTop: 16, letterSpacing: '-0.02em'}}>Five candidate brakes, ranked by <span style={{color: C.amber}}>convergent evidence</span>.</div>
      </div>

      <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
        {/* group headers + divider */}
        <g opacity={headP} fontFamily={sans}>
          <text x={(colX(0) + colX(3)) / 2} y={300} textAnchor="middle" fill={C.teal} fontSize={15} fontWeight={700} letterSpacing="0.14em">MEASURED IN THE CD4 SCREEN</text>
          <text x={(colX(4) + colX(6)) / 2} y={300} textAnchor="middle" fill={C.amber} fontSize={15} fontWeight={700} letterSpacing="0.14em">CURATED EXTERNAL EVIDENCE</text>
          <line x1={980} y1={318} x2={980} y2={rowY(4) + 46} stroke="rgba(255,255,255,0.1)" strokeWidth={1.2} strokeDasharray="4 6" />
        </g>
        {/* column headers (2-line) */}
        <g opacity={headP} fill={C.body} fontFamily={sans} fontSize={14} fontWeight={600}>
          {AXES.map((a, j) => a.split('\n').map((ln, k) => (
            <text key={`${j}-${k}`} x={colX(j)} y={338 + k * 18} textAnchor="middle">{ln}</text>
          )))}
        </g>
        {/* rows */}
        {ROWS.map((r, i) => (
          <g key={r.g}>
            <line x1={600} y1={rowY(i)} x2={1250} y2={rowY(i)} stroke="rgba(255,255,255,0.05)" strokeWidth={1} opacity={headP} />
            <text x={585} y={rowY(i) + 8} textAnchor="end" fill={C.ink} fontFamily={disp} fontWeight={700} fontSize={27} opacity={titleS}>{r.g}</text>
            {r.v.map((val, j) => {
              const s = spring({frame: frame - 40 - (i * 6 + j * 8), fps, config: {damping: 190, mass: 0.6}});
              return <circle key={j} cx={colX(j)} cy={rowY(i)} r={(7 + 21 * val) * s} fill={bubbleFill(val)} stroke="rgba(255,255,255,0.25)" strokeWidth={1.5} />;
            })}
          </g>
        ))}
      </svg>

      {/* call + note panel (right) */}
      {ROWS.map((r, i) => {
        const s = spring({frame: frame - 150 - i * 10, fps, config: {damping: 200}});
        const [bg, fg] = CHIP[r.cc];
        return (
          <div key={r.g} style={{position: 'absolute', left: 1290, top: rowY(i) - 34, width: 470, opacity: s, transform: `translateX(${(1 - s) * 14}px)`}}>
            <div style={{display: 'inline-block', fontFamily: disp, fontWeight: 700, fontSize: 16, letterSpacing: '0.04em', color: fg, background: bg, border: r.cc === 'amber' ? 'none' : `1px solid ${fg}44`, borderRadius: 999, padding: '5px 15px'}}>{r.call}</div>
            <div style={{fontSize: 18, color: C.mut, marginTop: 6, lineHeight: 1.3}}>{r.note}</div>
          </div>
        );
      })}

      {/* size legend */}
      <div style={{position: 'absolute', left: 130, bottom: 70, display: 'flex', alignItems: 'center', gap: 16, opacity: headP}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 10}}>
          {[0.25, 0.6, 1].map((v) => <svg key={v} width={2 * (7 + 21 * v)} height={2 * (7 + 21 * v)}><circle cx={7 + 21 * v} cy={7 + 21 * v} r={7 + 21 * v} fill={bubbleFill(v)} stroke="rgba(255,255,255,0.25)" strokeWidth={1.5} /></svg>)}
        </div>
        <div style={{fontSize: 20, color: C.mut}}>weaker → stronger evidence (0–1) · a curated summary, not a fitted model</div>
      </div>
    </AbsoluteFill>
  );
};
