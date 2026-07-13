# Written summary (submission)

**Brakepoint is a genome-scale discovery engine for cancer-immunotherapy drug targets.**

The best cancer immunotherapies cut the brakes off T cells, but only a handful have been drugged. Brakepoint hunts the rest — genome-wide.

It reads a public Marson (Gladstone)/Pritchard (Stanford) screen whole: 2.6 million human T cells, 12,449 genes each switched off. At this scale, standard analysis collapses — almost everything looks significant, and the biggest effects are machinery the cell needs to survive, not targets.

Brakepoint breaks the deadlock: measuring how hard each shutoff hits the cell and which way it pushes it — toward a stronger or weaker fighter — telling a real drug target from essential machinery.

With zero prior hints, it rediscovered CBLB — already racing into the clinic — then surfaced four more: CD5, DGKA, SMAD3, UBASH3A, each backed by seven independent lines of evidence.

One person built it in a week. Claude Science ran the analysis on an NVIDIA DGX Spark; one command reproduces every result; a self-audit caught and fixed a real bug before any conclusion.

The payoff: five candidate T-cell targets to test — a blueprint for AI-native drug discovery.

— Chengchen (Sam) Duan (duanchengchen@gmail.com · github.com/duanchengchen-oss)
