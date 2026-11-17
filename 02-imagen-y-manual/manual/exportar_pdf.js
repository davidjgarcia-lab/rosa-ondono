// Exporta manual-de-marca.html a PDF (A4 horizontal) y genera miniaturas de control.
// Uso: node exportar_pdf.js [--png]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1123, height: 794 } });
  await p.goto('file://' + path.join(__dirname, 'manual-de-marca.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(__dirname, 'manual-de-marca.pdf'), width: '297mm', height: '210mm', printBackground: true, preferCSSPageSize: true });
  if (process.argv.includes('--png')) {
    const out = process.env.PNG_DIR || __dirname;
    await p.emulateMedia({ media: 'print' });
    const pages = await p.$$('section.page');
    for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(out, `p${String(i + 1).padStart(2, '0')}.png`) });
  }
  await b.close();
  console.log('PDF generado');
})();
