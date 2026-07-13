import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {C, disp, sans} from '../theme';
import data from '../../public/donordata.json';

const PL = 585, PR = 1345, PT = 220, PB = 980; // square plot (equal aspect for the diagonal)
const LO = -1.25, HI = 0.65;
const xS = (v: number) => PL + ((v - LO) / (HI - LO)) * (PR - PL);
const yS = (v: number) => PB - ((v - LO) / (HI - LO)) * (PB - PT);

type Pt = {g: string; x: number; y: number; a: boolean};
const D = data as unknown as {bulk: [number, number][]; machinery: Pt[]; cand: Pt[]};
const LBL: Record<string, [number, number, string]> = {
  CBLB: [16, 5, 'start'], CD5: [15, -9, 'start'], DGKA: [-14, 20, 'end'],
  UBASH3A: [-15, -7, 'end'], SMAD3: [9, -13, 'start'],
};

export const Brakes: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const titleS = spring({frame, fps, config: {damping: 200}});
  const axisP = interpolate(frame, [8, 40], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const diagW = interpolate(frame, [26, 68], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const bulkOp = interpolate(frame, [22, 64], [0, 0.3], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const c1 = spring({frame: frame - 150, fps, config: {damping: 200}});
  const c2 = spring({frame: frame - 205, fps, config: {damping: 200}});

  return (
    <AbsoluteFill style={{backgroundColor: C.bg, fontFamily: sans}}>
      <AbsoluteFill style={{background:
        'radial-gradient(42% 50% at 14% 8%, rgba(13,148,136,0.20), transparent 60%),' +
        'radial-gradient(40% 46% at 90% 12%, rgba(217,122,18,0.12), transparent 62%)'}} />
      <div style={{position: 'absolute', top: 60, right: 130, fontFamily: disp, fontWeight: 600, letterSpacing: '0.3em', fontSize: 21, color: 'rgba(127,233,216,0.5)'}}>BRAKEPOINT</div>
      <div style={{position: 'absolute', top: 64, left: 130, width: 430, opacity: titleS, transform: `translateY(${(1 - titleS) * 18}px)`}}>
        <div style={{display: 'inline-flex', alignItems: 'center', gap: 12, fontSize: 18, fontWeight: 700, letterSpacing: '0.26em', textTransform: 'uppercase', color: C.teal, background: 'rgba(47,214,191,0.08)', border: '1px solid rgba(47,214,191,0.2)', padding: '9px 18px', borderRadius: 999}}>Reported honestly</div>
        <div style={{fontFamily: disp, fontWeight: 700, fontSize: 52, color: C.ink, marginTop: 16, letterSpacing: '-0.02em'}}>What <span style={{color: C.amber}}>two donors</span> can support.</div>
        <div style={{fontSize: 24, color: C.mut, marginTop: 20, lineHeight: 1.42}}>Each knockdown's direction, measured in <b style={{color: C.body}}>each donor</b> separately. On the diagonal = both donors agree.</div>
      </div>

      <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
        {/* origin crosshair */}
        <line x1={xS(0)} y1={PT} x2={xS(0)} y2={PB} stroke="#2b3633" strokeWidth={1.2} opacity={axisP} />
        <line x1={PL} y1={yS(0)} x2={PR} y2={yS(0)} stroke="#2b3633" strokeWidth={1.2} opacity={axisP} />
        {/* agreement diagonal */}
        <line x1={PL} y1={PB} x2={PL + (PR - PL) * diagW} y2={PB - (PB - PT) * diagW} stroke="#5b6b66" strokeWidth={1.6} strokeDasharray="8 8" />
        <text x={PR - 6} y={PT + 26} fill={C.mut} fontFamily={sans} fontSize={17} textAnchor="end" opacity={diagW} fontStyle="italic">agreement line</text>
        {/* bulk cloud */}
        <g opacity={bulkOp}>
          {D.bulk.map((p, i) => <circle key={i} cx={xS(p[0])} cy={yS(p[1])} r={3} fill="#cdccc4" />)}
        </g>
        {/* axes */}
        <g opacity={axisP} fill={C.mut} fontFamily={sans} fontSize={17}>
          {[-1, -0.5, 0, 0.5].map((v) => <text key={`x${v}`} x={xS(v)} y={PB + 32} textAnchor="middle">{v}</text>)}
          {[-1, -0.5, 0, 0.5].map((v) => <text key={`y${v}`} x={PL - 16} y={yS(v) + 5} textAnchor="end">{v}</text>)}
          <text x={(PL + PR) / 2} y={PB + 70} textAnchor="middle" fontSize={22} fill={C.mut}>Direction of effect · donor A</text>
          <text x={PL - 70} y={(PT + PB) / 2} textAnchor="middle" fontSize={22} fill={C.mut} transform={`rotate(-90 ${PL - 70} ${(PT + PB) / 2})`}>donor B</text>
        </g>
        {/* machinery (teal, lower-left cluster) */}
        {D.machinery.map((p, i) => {
          const s = spring({frame: frame - 78 - i * 4, fps, config: {damping: 180, mass: 0.6}});
          return <circle key={p.g} cx={xS(p.x)} cy={yS(p.y)} r={11} fill="#0d9488" stroke="#fff" strokeWidth={2.1} opacity={s} />;
        })}
        {/* candidates: circle = donor-consistent, diamond = donor-split */}
        {D.cand.map((p, i) => {
          const s = spring({frame: frame - 150 - i * 8, fps, config: {damping: 180, mass: 0.6}});
          const cx = xS(p.x), cy = yS(p.y), o = LBL[p.g];
          return (
            <g key={p.g} opacity={s} transform={`translate(${cx},${cy}) scale(${0.6 + 0.4 * s})`}>
              {p.a
                ? <circle r={12} fill="#f4b062" stroke="#fff" strokeWidth={2.2} />
                : <rect x={-11} y={-11} width={22} height={22} transform="rotate(45)" fill="#f4b062" stroke="#fff" strokeWidth={2.2} />}
              {o ? <text x={o[0]} y={o[1]} fill="#f4b062" fontFamily={disp} fontWeight={600} fontSize={22} textAnchor={o[2] as never} transform={`scale(${1 / (0.6 + 0.4 * s)})`}>{p.g}</text> : null}
            </g>
          );
        })}
      </svg>

      {/* legend */}
      <div style={{position: 'absolute', left: 130, top: 470, opacity: titleS}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 12, fontSize: 21, color: C.body, marginBottom: 14}}>
          <svg width={22} height={22}><circle cx={11} cy={11} r={9} fill="#f4b062" stroke="#fff" strokeWidth={2} /></svg>donor-consistent
        </div>
        <div style={{display: 'flex', alignItems: 'center', gap: 12, fontSize: 21, color: C.body}}>
          <svg width={22} height={22}><rect x={3} y={3} width={16} height={16} transform="rotate(45 11 11)" fill="#f4b062" stroke="#fff" strokeWidth={2} /></svg>donor-split (n = 2)
        </div>
      </div>

      {/* callout: machinery */}
      <div style={{position: 'absolute', left: 150, top: 760, width: 380, opacity: c1, transform: `translateY(${(1 - c1) * 16}px)`}}>
        <div style={{fontFamily: disp, fontWeight: 700, fontSize: 24, color: C.teal}}>Machinery: unanimous</div>
        <div style={{fontSize: 19, color: '#5bbfb2', marginTop: 4, lineHeight: 1.3}}>every TCR gene agrees in both donors — the axis is sound.</div>
      </div>
      {/* callout: candidates */}
      <div style={{position: 'absolute', right: 120, top: 700, width: 440, opacity: c2, transform: `translateY(${(1 - c2) * 16}px)`, textAlign: 'right'}}>
        <div style={{fontFamily: disp, fontWeight: 700, fontSize: 24, color: C.amber}}>CD5 · DGKA hold up</div>
        <div style={{fontSize: 19, color: '#c9903f', marginTop: 4, lineHeight: 1.34}}>CBLB, SMAD3, UBASH3A ride on one donor. A two-donor power limit — a shortlist to test, not a finished list.</div>
      </div>
    </AbsoluteFill>
  );
};
