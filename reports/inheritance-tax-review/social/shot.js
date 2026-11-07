const {chromium} = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1080, height: 1350}, deviceScaleFactor: 1});
  await p.goto('file://' + process.argv[2], {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  const ov = await p.evaluate(() => [...document.querySelectorAll('.s')].map((s, i) => {
    const bd = s.querySelector('.body,.cv'); return [i + 1, bd.scrollHeight - bd.clientHeight];
  }).filter(x => x[1] > 0));
  console.log('overflow', JSON.stringify(ov));
  const els = await p.$$('.s');
  for (let i = 0; i < els.length; i++)
    await els[i].screenshot({path: `${process.argv[3]}/IG_${String(i + 1).padStart(2, '0')}.png`});
  await b.close();
})();
