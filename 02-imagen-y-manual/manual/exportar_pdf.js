// Exporta manual-de-marca.html a PDF (A4). Uso: node exportar_pdf.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, 'manual-de-marca.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(__dirname, 'manual-de-marca.pdf'), format: 'A4', printBackground: true,
    margin: { top: '12mm', bottom: '14mm', left: '0', right: '0' },
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#701B78">Rosa Ondoño · Manual de marca · borrador v1 · <span class="pageNumber"></span>/<span class="totalPages"></span></div>' });
  await b.close();
  console.log('PDF generado');
})();
