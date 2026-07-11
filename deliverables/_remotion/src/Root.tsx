import React from 'react';
import {Composition} from 'remotion';
import {BrakepointVideo} from './BrakepointVideo';
import {TOTAL} from './timeline';

export const RemotionRoot: React.FC = () => (
  <Composition id="BrakepointVideo" component={BrakepointVideo}
    durationInFrames={TOTAL} fps={30} width={1920} height={1080} />
);
