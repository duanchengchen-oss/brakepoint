import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {DUR, TR} from './timeline';
import {Title} from './scenes/Title';
import {Question} from './scenes/Question';
import {Provenance} from './scenes/Provenance';
import {Significance} from './scenes/Significance';
import {Method} from './scenes/Method';
import {Validation} from './scenes/Validation';
import {MapScene} from './scenes/MapScene';
import {Explorer} from './scenes/Explorer';
import {VsTraditional} from './scenes/VsTraditional';
import {Brakes} from './scenes/Brakes';
import {Close} from './scenes/Close';

const SCENES = [Title, Question, Provenance, Significance, MapScene, Explorer, VsTraditional, Method, Validation, Brakes, Close];

export const BrakepointVideo: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: '#0a1211'}}>
    <TransitionSeries>
      {SCENES.map((Scene, i) => (
        <React.Fragment key={i}>
          <TransitionSeries.Sequence durationInFrames={DUR[i]}>
            <Scene />
            <Sequence from={12}>
              <Audio src={staticFile(`audio/slide_${i}.mp3`)} />
            </Sequence>
          </TransitionSeries.Sequence>
          {i < SCENES.length - 1 ? (
            <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames: TR})} />
          ) : null}
        </React.Fragment>
      ))}
    </TransitionSeries>
  </AbsoluteFill>
);
