// Mostrar/ocultar anotaciones UX (no forma parte del diseño final)
document.addEventListener('DOMContentLoaded',()=>{
  const b=document.createElement('button');b.className='btn sec annot-toggle';b.type='button';
  b.setAttribute('aria-pressed','true');b.textContent='Anotaciones: sí';
  b.onclick=()=>{const off=document.body.classList.toggle('no-annot');b.setAttribute('aria-pressed',String(!off));b.textContent='Anotaciones: '+(off?'no':'sí')};
  document.body.appendChild(b);
  // Selección de hueco en la maqueta de reserva
  document.querySelectorAll('.slot:not(:disabled)').forEach(s=>s.addEventListener('click',()=>{
    s.closest('.slots').querySelectorAll('.slot').forEach(o=>o.setAttribute('aria-pressed','false'));
    s.setAttribute('aria-pressed','true');}));
});
