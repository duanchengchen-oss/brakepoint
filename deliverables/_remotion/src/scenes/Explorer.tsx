import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile, useVideoConfig, useCurrentFrame, spring} from 'remotion';
import {Bg, Eyebrow, useEnter} from '../lib/anim';
import {C, disp, sans} from '../theme';

// trimmed screen-recording of the live explorer (1280x820, ~10.5s @30fps)
const VIDEO_FRAMES = 316;
const VW = 1280, VH = 820;

const Row: React.FC<{delay: number; k: string; label: string; color: string}> = ({delay, k, label, color}) => {
  const e = useEnter(delay, 24);
  return (
    <div style={{...e, display: 'flex', gap: 18, alignItems: 'flex-start'}}>
      <div style={{flex: 'none', marginTop: 4, fontFamily: 'ui-monospace, monospace', fontSize: 20, fontWeight: 700,
        color, background: 'rgba(255,255,255,0.05)', border: `1px solid ${color}55`, borderRadius: 10, padding: '6px 14px'}}>{k}</div>
      <div style={{fontSize: 29, lineHeight: 1.32, color: C.body}}>{label}</div>
    </div>
  );
};

export const Explorer: React.FC = () => {
  const {durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();
  // stretch the clip to span the whole scene (slight slow-down aids readability); the
  // scene-end crossfade masks the final frame.
  const rate = VIDEO_FRAMES / durationInFrames;

  const disp0 = 980; // browser-frame content width
  const scale = disp0 / VW; // 0.766
  const vh = VH * scale;
  const frameS = spring({frame: frame - 6, fps: 30, config: {damping: 200, mass: 0.8}});

  return (
    <Bg>
      <Eyebrow>Explore · the live leaderboard</Eyebrow>
      <div style={{display: 'flex', gap: 66, alignItems: 'center', flex: 1, marginTop: 26}}>
        {/* left — a browser frame playing the real explorer */}
        <div style={{
          flex: 'none', width: disp0 + 36, opacity: frameS, transform: `translateY(${(1 - frameS) * 22}px)`,
          background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 26, padding: 8,
          boxShadow: '0 40px 120px rgba(0,0,0,0.5)'}}>
          <div style={{background: '#0c1614', borderRadius: 19, overflow: 'hidden', border: '1px solid rgba(255,255,255,0.06)'}}>
            {/* title bar */}
            <div style={{display: 'flex', alignItems: 'center', gap: 10, padding: '14px 18px', borderBottom: '1px solid rgba(255,255,255,0.06)'}}>
              <div style={{width: 12, height: 12, borderRadius: 999, background: '#e0645c'}} />
              <div style={{width: 12, height: 12, borderRadius: 999, background: '#e2b24a'}} />
              <div style={{width: 12, height: 12, borderRadius: 999, background: '#3fbf7f'}} />
              <div style={{marginLeft: 18, flex: 1, textAlign: 'center', fontFamily: sans, fontSize: 18, color: C.mut,
                background: 'rgba(255,255,255,0.04)', borderRadius: 999, padding: '6px 0'}}>brakepoint · explore — 11,438 knockdowns, live</div>
            </div>
            <div style={{width: disp0, height: vh, overflow: 'hidden', margin: '0 auto'}}>
              <OffthreadVideo src={staticFile('explorer.mp4')} playbackRate={rate}
                style={{width: disp0, height: vh, display: 'block'}} />
            </div>
          </div>
        </div>

        {/* right — what you're seeing */}
        <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 30}}>
          <div style={{fontFamily: disp, fontWeight: 700, fontSize: 52, lineHeight: 1.06, letterSpacing: '-0.02em', color: C.ink}}>
            Not a picture.<br/>The real leaderboard.
          </div>
          <div style={{...useEnter(20, 20), fontSize: 27, lineHeight: 1.4, color: C.mut}}>
            Every point is one CRISPRi knockdown, placed by what it actually did to the cell.
          </div>
          <div style={{display: 'flex', flexDirection: 'column', gap: 22, marginTop: 4}}>
            <Row delay={34} k="type" label="Search any gene — it lights up on the map." color={C.amber} />
            <Row delay={48} k="hover" label="Read its causal effect and its direction." color={C.teal} />
            <Row delay={62} k="axes" label="Machinery sits negative · candidate brakes sit positive." color={C.body} />
          </div>
        </div>
      </div>
    </Bg>
  );
};
