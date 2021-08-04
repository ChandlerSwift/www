---
layout: post
title: New Relic and AppFog v2
---

CenturyLink’s AppFog v2 is supposed to have great support for New Relic.
However, their documentation leaves a bit to be desired. Don’t be dissuaded:
the setup process is almost comically simple. Here are the steps to set up
AppFog with New Relic:

 * First, sign up for New Relic (if you haven’t already) at
   [newrelic.com/appfog][https://newrelic.com/appfog].
 * Go to to the “APM” (*A*pplication *P*erformance *M*onitoring) section to
   create a new app.
 * Select your language.
 * Under step 1, click Reveal License Key.

That’s all we need from New Relic. Now it’s on to AppFog:

`cf set-env [your-app-name] NEWRELIC_LICENSE: [your license key]`

And you’re done! In about five minutes, the stats should start rolling in.

(A note: In my case, New Relic kept a warning on that page that no data had been
received, so the app might not have been set up correctly. I bypassed this and
manually reloaded, and it worked regardless.)
