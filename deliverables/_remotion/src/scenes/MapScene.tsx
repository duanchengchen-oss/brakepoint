import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {C, disp, sans} from '../theme';
import data from '../../public/mapdata.json';

const PL = 210, PR = 1800, PT = 210, PB = 980; // plot rect
const XMAX = (data as any).xmax as number;
const YMIN = (data as any).ymin as number, YMAX = (data as any).ymax as number;
const xS = (e: number) => PL + ((e - -1.5) / (XMAX - -1.5)) * (PR - PL);
const yS = (d: number) => PB - ((d - YMIN) / (YMAX - YMIN)) * (PB - PT);

type Pt = {g: string; x: number; y: number; a: boolean};
const OFF: Record<string, [number, number, string]> = {
  ZAP70: [16, 4, 'start'], LCP2: [16, 16, 'start'], CD3E: [0, 34, 'middle'], CD3G: [6, -22, 'start'],
  PLCG1: [-10, 34, 'end'], LAT: [0, 36, 'middle'], VAV1: [-8, -20, 'end'], CD3D: [-12, 34, 'end'],
  CD247: [18, 26, 'start'], ITK: [-16, 26, 'end'],
  SMAD3: [18, 16, 'start'], LAT2: [18, 8, 'start'], CBLB: [-14, -26, 'end'], CD5: [20, 12, 'start'], DGKA: [8, 30, 'start'],
};

export const MapScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const bulk = (data as any).bulk as [number, number][];
  const mach = (data as any).machinery as Pt[];
  const brk = (data as any).brakes as Pt[];

  const titleS = spring({frame, fps, config: {damping: 200}});
  const axisP = interpolate(frame, [8, 40], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const bulkOp = interpolate(frame, [22, 70], [0, 0.34], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const zeroW = interpolate(frame, [30, 70], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const upCap = interpolate(frame, [60, 90], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const dnCap = interpolate(frame, [110, 145], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const calloutS = spring({frame: frame - 250, fps, config: {damping: 200}});
  const sig2 = interpolate(frame, [498, 540], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  const y0 = yS(0);
  return (
    <AbsoluteFill style={{backgroundColor: C.bg, fontFamily: sans}}>
      <div style={{position: 'absolute', top: 60, right: 130, fontFamily: disp, fontWeight: 600, letterSpacing: '0.3em', fontSize: 21, color: 'rgba(127,233,216,0.5)'}}>BRAKEPOINT</div>
      <div style={{position: 'absolute', top: 70, left: 130, opacity: titleS, transform: `translateY(${(1 - titleS) * 18}px)`}}>
        <div style={{fontFamily: disp, fontWeight: 600, fontSize: 40, color: C.ink}}>A genome-scale signed causal map</div>
        <div style={{fontSize: 22, color: C.mut, marginTop: 8}}>2,638,736 primary human CD4⁺ T cells · 12,449 CRISPRi knockdowns · built with Claude Science</div>
      </div>

      <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
        {/* quadrant washes */}
        <rect x={PL} y={PT} width={PR - PL} height={y0 - PT} fill="#d97a12" opacity={0.05 * upCap} />
        <rect x={PL} y={y0} width={PR - PL} height={PB - y0} fill="#0d9488" opacity={0.06 * dnCap} />
        {/* bulk cloud */}
        <g opacity={bulkOp}>
          {bulk.map((p, i) => <circle key={i} cx={xS(p[0])} cy={yS(p[1])} r={3} fill="#cdccc4" />)}
        </g>
        {/* y=0 sign line */}
        <line x1={PL} y1={y0} x2={PL + (PR - PL) * zeroW} y2={y0} stroke="#52514e" strokeWidth={2} />
        {/* axis ticks */}
        <g opacity={axisP} fill={C.mut} fontFamily={sans} fontSize={18}>
          {[-0.8, -0.4, 0, 0.4].map((v) => (
            <text key={v} x={PL - 14} y={yS(v) + 6} textAnchor="end">{v.toFixed(1)}</text>
          ))}
          {[0, 20, 40, 60].map((e) => (
            <text key={e} x={xS(e)} y={PB + 30} textAnchor="middle">{e}</text>
          ))}
        </g>
        {/* axis labels */}
        <g opacity={axisP} fill={C.mut} fontFamily={sans} fontSize={22}>
          <text x={(PL + PR) / 2} y={1050} textAnchor="middle">Causal effect size  ·  E-distance</text>
          <text x={148} y={(PT + PB) / 2} textAnchor="middle" transform={`rotate(-90 148 ${(PT + PB) / 2})`}>Direction of effect  ·  effector − dysfunction</text>
        </g>
        {/* machinery (teal) */}
        {mach.map((p, i) => {
          const s = spring({frame: frame - 95 - i * 5, fps, config: {damping: 180, mass: 0.6}});
          const cx = xS(p.x), cy = yS(p.y);
          const o = OFF[p.g] || [12, 0, 'start'];
          return (
            <g key={p.g} opacity={s}>
              <circle cx={cx} cy={cy + (1 - s) * 30} r={13} fill="#0d9488" stroke="#fff" strokeWidth={2.4} />
              <text x={cx + o[0]} y={cy + o[1]} fill="#0b6b62" fontFamily={disp} fontWeight={600} fontSize={26} textAnchor={o[2] as any}>{p.g}</text>
            </g>
          );
        })}
        {/* brakes (amber) — circle=consistent, diamond=donor-split */}
        {brk.map((p, i) => {
          const s = spring({frame: frame - 300 - i * 7, fps, config: {damping: 180, mass: 0.6}});
          const cx = xS(p.x), cy = yS(p.y);
          const o = OFF[p.g] || [12, 0, 'start'];
          return (
            <g key={p.g} opacity={s} transform={`translate(${cx},${cy}) scale(${0.6 + 0.4 * s})`}>
              {p.a
                ? <circle r={12} fill="#d97a12" stroke="#fff" strokeWidth={2.4} />
                : <rect x={-11} y={-11} width={22} height={22} transform="rotate(45)" fill="#d97a12" stroke="#fff" strokeWidth={2.4} />}
              <text x={o[0]} y={o[1]} fill="#a85c08" fontFamily={disp} fontWeight={600} fontSize={26} textAnchor={o[2] as any} transform={`scale(${1 / (0.6 + 0.4 * s)})`}>{p.g}</text>
            </g>
          );
        })}
      </svg>

      {/* quadrant captions */}
      <div style={{position: 'absolute', right: 130, top: yS(YMAX) + 6, textAlign: 'right', opacity: upCap}}>
        <div style={{fontFamily: disp, fontWeight: 600, fontSize: 30, color: C.amber}}>knockdown ENHANCES the effector program</div>
        <div style={{fontSize: 24, color: '#c9903f', marginTop: 6, fontStyle: 'italic'}}>the positive quadrant · reported honestly</div>
      </div>
      <div style={{position: 'absolute', right: 130, top: y0 + 16, textAlign: 'right', opacity: dnCap}}>
        <div style={{fontFamily: disp, fontWeight: 600, fontSize: 30, color: C.teal}}>knockdown IMPAIRS the effector program</div>
        <div style={{fontSize: 24, color: '#5bbfb2', marginTop: 6, fontStyle: 'italic'}}>required machinery · not druggable</div>
      </div>

      {/* headline callout — content crossfades in place (stays clear of both captions) */}
      <div style={{position: 'absolute', left: 806, top: 300, width: 588, opacity: calloutS, transform: `translateY(${(1 - calloutS) * 20}px)`,
        background: 'rgba(252,252,251,0.97)', borderRadius: 20, padding: '26px 32px', boxShadow: '0 20px 60px rgba(0,0,0,0.4)'}}>
        <div style={{opacity: 1 - sig2}}>
          <div style={{fontFamily: disp, fontWeight: 700, fontSize: 29, color: '#0b1220'}}>14 of the 15 largest-effect knockdowns</div>
          <div style={{fontSize: 23, color: '#39424e', marginTop: 8, lineHeight: 1.34}}>impair effector function — magnitude alone would nominate the cell's own machinery.</div>
        </div>
        <div style={{position: 'absolute', left: 32, right: 32, top: 26, opacity: sig2}}>
          <div style={{fontFamily: disp, fontWeight: 700, fontSize: 29, color: '#0b6b62'}}>97.5% of tested knockdowns clear significance</div>
          <div style={{fontSize: 23, color: '#39424e', marginTop: 8, lineHeight: 1.34}}>at 2.6 M cells — so we rank by <b>effect size</b>, not p-value.</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
