import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {C, disp, sans} from '../theme';
import data from '../../public/sigdata.json';

const PL = 235, PR = 1770, PT = 305, PB = 930;
const XMIN = -2, XMAX = (data as {xmax: number}).xmax;
const YMAX = (data as {ymax: number}).ymax;
const xS = (e: number) => PL + ((e - XMIN) / (XMAX - XMIN)) * (PR - PL);
const yS = (v: number) => PB - (v / YMAX) * (PB - PT);

type Pt = {g: string; x: number; y: number};
const D = data as unknown as {
  bulk: [number, number][]; machinery: Pt[]; cand: Pt[];
  qline: number; pctSig: number; nFloor: number; perm: number; n: number;
};

export const Significance: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const titleS = spring({frame, fps, config: {damping: 200}});
  const axisP = interpolate(frame, [8, 40], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const bulkOp = interpolate(frame, [22, 66], [0, 0.34], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const bandOp = interpolate(frame, [46, 82], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const lineW = interpolate(frame, [30, 70], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const c1 = spring({frame: frame - 165, fps, config: {damping: 200}});
  const c2 = spring({frame: frame - 220, fps, config: {damping: 200}});

  const qy = yS(D.qline);
  return (
    <AbsoluteFill style={{backgroundColor: C.bg, fontFamily: sans}}>
      <AbsoluteFill style={{background:
        'radial-gradient(42% 50% at 15% 6%, rgba(13,148,136,0.22), transparent 60%),' +
        'radial-gradient(40% 46% at 88% 10%, rgba(217,122,18,0.12), transparent 62%)'}} />
      <div style={{position: 'absolute', top: 60, right: 130, fontFamily: disp, fontWeight: 600, letterSpacing: '0.3em', fontSize: 21, color: 'rgba(127,233,216,0.5)'}}>BRAKEPOINT</div>
      <div style={{position: 'absolute', top: 64, left: 130, opacity: titleS, transform: `translateY(${(1 - titleS) * 18}px)`}}>
        <div style={{display: 'inline-flex', alignItems: 'center', gap: 12, fontSize: 18, fontWeight: 700, letterSpacing: '0.26em', textTransform: 'uppercase', color: C.teal, background: 'rgba(47,214,191,0.08)', border: '1px solid rgba(47,214,191,0.2)', padding: '9px 18px', borderRadius: 999}}>The trap · significance</div>
        <div style={{fontFamily: disp, fontWeight: 700, fontSize: 54, color: C.ink, marginTop: 16, letterSpacing: '-0.02em'}}>Significance can't rank a <span style={{color: C.teal}}>million-cell screen</span>.</div>
      </div>

      <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
        <rect x={PL} y={PT} width={PR - PL} height={qy - PT} fill="#8fa39d" opacity={0.06 * bandOp} />
        <g opacity={bulkOp}>
          {D.bulk.map((p, i) => <circle key={i} cx={xS(p[0])} cy={yS(p[1])} r={3} fill="#cdccc4" />)}
        </g>
        <line x1={PL} y1={qy} x2={PL + (PR - PL) * lineW} y2={qy} stroke="#5b6b66" strokeWidth={1.5} strokeDasharray="7 7" />
        <text x={PR} y={qy - 12} fill={C.mut} fontFamily={sans} fontSize={17} textAnchor="end" opacity={lineW}>q = 0.05</text>
        <g opacity={axisP} fill={C.mut} fontFamily={sans} fontSize={18}>
          {[0, 20, 40, 60].map((e) => <text key={e} x={xS(e)} y={PB + 34} textAnchor="middle">{e}</text>)}
          {[1, 2, 3].map((v) => <text key={v} x={PL - 16} y={yS(v) + 6} textAnchor="end">{v.toFixed(1)}</text>)}
          <text x={(PL + PR) / 2} y={1028} textAnchor="middle" fontSize={22}>Causal effect size  ·  E-distance (power-equalized)</text>
          <text x={150} y={(PT + PB) / 2} textAnchor="middle" fontSize={22} transform={`rotate(-90 150 ${(PT + PB) / 2})`}>Statistical significance  ·  −log₁₀(q)</text>
        </g>
        {/* machinery (teal) — dense at the ceiling, so no per-point labels (callout names them) */}
        {D.machinery.map((p, i) => {
          const s = spring({frame: frame - 82 - i * 4, fps, config: {damping: 180, mass: 0.6}});
          return <circle key={p.g} cx={xS(p.x)} cy={yS(p.y)} r={12} fill="#0d9488" stroke="#fff" strokeWidth={2.2} opacity={s} />;
        })}
        {/* candidates (amber) — label the lead only */}
        {D.cand.map((p, i) => {
          const s = spring({frame: frame - 150 - i * 9, fps, config: {damping: 180, mass: 0.6}});
          const cx = xS(p.x), cy = yS(p.y);
          return (
            <g key={p.g} opacity={s}>
              <circle cx={cx} cy={cy} r={12} fill="#f4b062" stroke="#fff" strokeWidth={2.2} />
              {p.g === 'CBLB' ? <text x={cx - 15} y={cy - 15} fill="#f4b062" fontFamily={disp} fontWeight={700} fontSize={23} textAnchor="end">CBLB</text> : null}
            </g>
          );
        })}
      </svg>

      <div style={{position: 'absolute', left: PL, top: PT - 46, width: PR - PL, textAlign: 'center', opacity: bandOp, fontFamily: disp, fontWeight: 600, fontSize: 25, color: C.body}}>
        significance ceiling — {D.pctSig}% clear q &lt; 0.05 · {D.nFloor.toLocaleString()} pile at the permutation floor
      </div>

      {/* callout: candidate cluster (sparse lower-middle) */}
      <div style={{position: 'absolute', left: 470, top: 605, width: 470, opacity: c1, transform: `translateY(${(1 - c1) * 16}px)`, background: 'rgba(252,252,251,0.97)', borderRadius: 16, padding: '18px 24px', boxShadow: '0 18px 50px rgba(0,0,0,0.42)'}}>
        <div style={{fontFamily: disp, fontWeight: 700, fontSize: 23, color: '#a85c08'}}>candidate brakes</div>
        <div style={{fontSize: 19, color: '#39424e', marginTop: 5, lineHeight: 1.32}}>modest-to-moderate effect — not brake-enriched (Mann–Whitney p = 0.70)</div>
      </div>
      {/* callout: machinery (right) */}
      <div style={{position: 'absolute', right: 150, top: 455, width: 380, opacity: c2, transform: `translateY(${(1 - c2) * 16}px)`, textAlign: 'right'}}>
        <div style={{fontFamily: disp, fontWeight: 700, fontSize: 25, color: C.teal}}>TCR machinery</div>
        <div style={{fontSize: 19, color: '#5bbfb2', marginTop: 4, lineHeight: 1.3}}>the largest effects — required, not druggable brakes</div>
      </div>
    </AbsoluteFill>
  );
};
