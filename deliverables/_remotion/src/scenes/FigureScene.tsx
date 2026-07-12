import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig, spring} from 'remotion';
import {Bg, Eyebrow, Words} from '../lib/anim';
import {C} from '../theme';
export const FigureScene: React.FC<{eyebrow: string; title: {t: string; color?: string}[]; img: string; caption?: string; titleSize?: number}> =
({eyebrow, title, img, caption, titleSize = 50}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - 12, fps, config: {damping: 200}});
  return (
    <Bg>
      <Eyebrow>{eyebrow}</Eyebrow>
      <div style={{marginTop: 14}}><Words size={titleSize} delay={8} maxWidth={1520} parts={title} /></div>
      <div style={{flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', marginTop: 12,
        opacity: s, transform: `translateY(${(1 - s) * 24}px)`}}>
        <div style={{background: 'rgba(255,255,255,0.06)', border: `1px solid ${C.line}`, padding: 14, borderRadius: 26}}>
          <div style={{background: '#fcfcfb', borderRadius: 15, overflow: 'hidden', lineHeight: 0}}>
            <Img src={staticFile(`figures/${img}`)} style={{display: 'block', maxWidth: 1560, maxHeight: 600, width: 'auto', height: 'auto'}} />
          </div>
        </div>
      </div>
      {caption ? <div style={{fontSize: 22, color: C.mut, marginTop: 4}}>{caption}</div> : null}
    </Bg>
  );
};
