---
title: "AIRduino Guitar"
tagline: "Physical Computing at Chalmers"
description: "A wearable Arduino air guitar: a glove sets the note, a stick with an accelerometer strums it."
tags: [open-source, arduino, processing, music, electronics]
---

The AIRduino Guitar is a wearable virtual guitar that David Fournier, Monireh Sanaei, Maziar Shelbaf, Gustav Sohtell and I built in a two-week Physical Computing course project at Chalmers University. You shake a stick with an accelerometer in it to strum. The glove has four buttons, and an ultrasonic sensor measures the distance between your hands: together they set the pitch, a bit like frets on a guitar neck. Two analog inputs set the sustain and how hard you need to strum. The Arduino plays back a sampled guitar waveform through PWM, with a timer interrupt setting the pitch. The [Instructable](http://www.instructables.com/id/How-to-build-an-Air-Guitar-with-Arduino-aka-the-A/) shows how to build one.

<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/sJxM18o9EPs" title="AIRduino Guitar" allowfullscreen></iframe></div>

Watch it on YouTube: [AIRduino Guitar](https://www.youtube.com/watch?v=sJxM18o9EPs)

Source on GitHub: [Jell/airguitar](https://github.com/Jell/airguitar)
