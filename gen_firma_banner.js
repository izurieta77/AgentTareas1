const sharp = require('sharp');
const W=760, H=205;
const G = "url(#gold)";
const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<defs>
 <linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#9c7321"/>
   <stop offset="45%" stop-color="#f6e290"/>
   <stop offset="55%" stop-color="#f3da7e"/>
   <stop offset="100%" stop-color="#8c6418"/>
 </linearGradient>
 <linearGradient id="goldH" x1="0" y1="0" x2="1" y2="0">
   <stop offset="0%" stop-color="#b8902f"/>
   <stop offset="50%" stop-color="#f6e290"/>
   <stop offset="100%" stop-color="#b8902f"/>
 </linearGradient>
</defs>
<rect x="0" y="0" width="${W}" height="${H}" fill="#0d0d0d"/>
<rect x="3" y="3" width="${W-6}" height="${H-6}" fill="none" stroke="#7c5e20" stroke-width="1"/>

<!-- EMBLEM panel -->
<g transform="translate(16,26)">
  <rect x="0" y="0" width="120" height="150" fill="none" stroke="#6e5418" stroke-width="1"/>
  <!-- classical doorway / column (left) -->
  <g stroke="${G}" fill="none" stroke-width="2">
    <rect x="16" y="20" width="34" height="112"/>
    <line x1="16" y1="20" x2="50" y2="20"/>
    <rect x="13" y="12" width="40" height="9" fill="${G}"/>
    <line x1="24" y1="28" x2="24" y2="126"/>
    <line x1="33" y1="28" x2="33" y2="126"/>
    <line x1="42" y1="28" x2="42" y2="126"/>
  </g>
  <!-- flame (right) -->
  <path d="M86 130 C66 108 92 96 80 70 C100 86 96 50 88 36 C112 58 110 104 96 122 C94 126 90 130 86 130 Z"
        fill="${G}" stroke="#6e5418" stroke-width="0.6"/>
  <path d="M88 122 C80 110 92 104 86 92 C96 100 95 84 90 74 C103 90 100 110 92 120 Z" fill="#0d0d0d" opacity="0.35"/>
</g>

<!-- gold divider -->
<line x1="156" y1="24" x2="156" y2="181" stroke="#7c5e20" stroke-width="1.5"/>

<!-- NAME + TITLE -->
<text x="182" y="56" font-family="'DejaVu Serif',serif" font-size="27" font-weight="bold" fill="${G}">Lic. Eduardo Izurieta Martínez</text>
<text x="184" y="80" font-family="'DejaVu Sans',sans-serif" font-size="13" letter-spacing="0.5" fill="#cfa94e">CEO Partner · Consulting Assistant · Business Entrepreneur</text>

<!-- contacts -->
<g font-family="'DejaVu Sans',sans-serif" font-size="13" fill="#e9d9a6">
  <!-- row1 -->
  <g transform="translate(184,108)">
     <circle cx="7" cy="-4" r="7" fill="none" stroke="${G}" stroke-width="1.2"/>
     <line x1="0" y1="-4" x2="14" y2="-4" stroke="${G}" stroke-width="1.2"/>
     <ellipse cx="7" cy="-4" rx="3" ry="7" fill="none" stroke="${G}" stroke-width="1.2"/>
     <text x="22" y="0">asturvent-web.netlify.app</text>
  </g>
  <g transform="translate(454,108)">
     <circle cx="7" cy="-4" r="7" fill="none" stroke="${G}" stroke-width="1.2"/>
     <line x1="0" y1="-4" x2="14" y2="-4" stroke="${G}" stroke-width="1.2"/>
     <ellipse cx="7" cy="-4" rx="3" ry="7" fill="none" stroke="${G}" stroke-width="1.2"/>
     <text x="22" y="0">www.morgangasolineros.com.mx</text>
  </g>
  <!-- row2 -->
  <g transform="translate(184,138)">
     <rect x="0" y="-11" width="15" height="11" fill="none" stroke="${G}" stroke-width="1.2"/>
     <path d="M0 -11 L7.5 -4 L15 -11" fill="none" stroke="${G}" stroke-width="1.2"/>
     <text x="22" y="0">macs@morgangasolineros.com.mx</text>
  </g>
  <g transform="translate(454,138)">
     <rect x="0" y="-11" width="15" height="11" fill="none" stroke="${G}" stroke-width="1.2"/>
     <path d="M0 -11 L7.5 -4 L15 -11" fill="none" stroke="${G}" stroke-width="1.2"/>
     <text x="22" y="0">izurieta77@gmail.com</text>
  </g>
  <!-- row3 -->
  <g transform="translate(184,168)">
     <circle cx="7" cy="-4" r="7.5" fill="none" stroke="${G}" stroke-width="1.2"/>
     <line x1="7" y1="-4" x2="7" y2="-9" stroke="${G}" stroke-width="1.2"/>
     <line x1="7" y1="-4" x2="11" y2="-4" stroke="${G}" stroke-width="1.2"/>
     <text x="22" y="0">WhatsApp 55 4797 7723</text>
  </g>
</g>

<!-- bottom flourish -->
<g transform="translate(380,191)">
  <line x1="-60" y1="0" x2="-8" y2="0" stroke="#7c5e20" stroke-width="1"/>
  <circle cx="0" cy="0" r="3.5" fill="none" stroke="${G}" stroke-width="1.2"/>
  <line x1="8" y1="0" x2="60" y2="0" stroke="#7c5e20" stroke-width="1"/>
</g>
</svg>`;
require('fs').writeFileSync('/tmp/sig.svg', svg);
sharp(Buffer.from(svg)).jpeg({quality:92}).toFile('/home/user/AgentTareas1/firma-eduardo-banner.jpg')
 .then(i=>console.log('OK',i.width+'x'+i.height,i.size,'bytes')).catch(e=>{console.error(e);process.exit(1);});
