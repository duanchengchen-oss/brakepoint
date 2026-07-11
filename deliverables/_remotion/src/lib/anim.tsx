import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Img, staticFile} from 'remotion';
import {C, disp, sans} from '../theme';

// spring-based entrance: returns opacity + translateY(px)
export const useEnter = (delay = 0, dist = 40) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - delay, fps, config: {damping: 200, mass: 0.8}});
  return {opacity: s, transform: `translateY(${(1 - s) * dist}px)`};
};

// scene background: deep teal-black + two radial glows (slow drift) + faint grid + wordmark
export const Bg: React.FC<{children: React.ReactNode; glowAmber?: boolean}> = ({children, glowAmber = true}) => {
  const frame = useCurrentFrame();
  const drift = Math.sin(frame / 90) * 30;
  return (
    <AbsoluteFill style={{backgroundColor: C.bg, fontFamily: sans, overflow: 'hidden'}}>
      <AbsoluteFill style={{
        background:
          `radial-gradient(48% 60% at ${16 + drift / 20}% 8%, rgba(13,148,136,0.32), transparent 60%)` +
          (glowAmber ? `, radial-gradient(45% 52% at ${88 - drift / 30}% 26%, rgba(217,122,18,0.17), transparent 62%)` : ''),
      }} />
      <AbsoluteFill style={{
        opacity: 0.4,
        backgroundImage:
          'linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px)',
        backgroundSize: '70px 70px',
        WebkitMaskImage: 'radial-gradient(75% 70% at 30% 25%, #000, transparent 78%)',
      }} />
      <div style={{position: 'absolute', top: 60, right: 130, fontFamily: disp, fontWeight: 600,
        letterSpacing: '0.3em', fontSize: 21, color: 'rgba(127,233,216,0.5)'}}>BRAKEPOINT</div>
      <AbsoluteFill style={{padding: '118px 130px'}}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};

export const Eyebrow: React.FC<{children: React.ReactNode; delay?: number}> = ({children, delay = 0}) => {
  const e = useEnter(delay);
  return (
    <div style={{...e, display: 'inline-flex', alignSelf: 'flex-start', alignItems: 'center', gap: 12,
      fontSize: 19, fontWeight: 700, letterSpacing: '0.26em', textTransform: 'uppercase', color: C.teal,
      background: 'rgba(47,214,191,0.08)', border: '1px solid rgba(47,214,191,0.2)', padding: '11px 22px', borderRadius: 999}}>
      {children}
    </div>
  );
};

// count-up integer with thousands separators
export const CountUp: React.FC<{to: number; delay?: number; dur?: number; style?: React.CSSProperties}> = ({to, delay = 0, dur = 40, style}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame - delay, [0, dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const eased = 1 - Math.pow(1 - p, 3);
  const v = Math.round(eased * to);
  return <span style={style}>{v.toLocaleString('en-US')}</span>;
};

// staggered word reveal for a heading. `parts` = array of {t, color?}
export const Words: React.FC<{parts: {t: string; color?: string}[]; size: number; delay?: number; maxWidth?: number}> = ({parts, size, delay = 0, maxWidth}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const words: {t: string; color?: string}[] = [];
  parts.forEach((p) => p.t.split(' ').forEach((w, i) => words.push({t: (i === 0 ? '' : ' ') + w, color: p.color})));
  return (
    <div style={{fontFamily: disp, fontWeight: 700, fontSize: size, lineHeight: 1.04, letterSpacing: '-0.025em', color: C.ink, maxWidth}}>
      {words.map((w, i) => {
        const s = spring({frame: frame - delay - i * 3, fps, config: {damping: 200, mass: 0.7}});
        return (
          <span key={i} style={{display: 'inline-block', whiteSpace: 'pre', opacity: s, transform: `translateY(${(1 - s) * 26}px)`, color: w.color || C.ink}}>{w.t}</span>
        );
      })}
    </div>
  );
};

export const Bullet: React.FC<{children: React.ReactNode; color: string; delay?: number}> = ({children, color, delay = 0}) => {
  const e = useEnter(delay, 30);
  return (
    <div style={{...e, display: 'flex', gap: 22, alignItems: 'flex-start', fontSize: 33, lineHeight: 1.35, color: C.body}}>
      <div style={{flex: 'none', width: 16, height: 16, borderRadius: 6, marginTop: 14, background: color}} />
      <div>{children}</div>
    </div>
  );
};

export const Spacer: React.FC<{f?: number}> = ({f = 1}) => <div style={{flex: f}} />;
