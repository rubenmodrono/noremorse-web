// Utilidades comunes a todos los Reels de nØr3mors3
const H={1:"#35d6c0",2:"#3bd48a",3:"#7bd44b",4:"#c3d43b",5:"#f0c030",6:"#f29a30",7:"#f06a45",8:"#ee4f7a",9:"#d84fb8",10:"#a465e8",11:"#6a7ae8",12:"#3da0e8"};
const col=k=>H[parseInt(k)];
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)), seg=(t,a,b)=>clamp((t-a)/(b-a));
const ease=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2, out=x=>1-Math.pow(1-x,3);
const $=id=>document.getElementById(id);
const NS='http://www.w3.org/2000/svg';
function el(n,a,p){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);(p||$('svg')).appendChild(e);return e}
function cr(P){let d=`M${P[0][0]},${P[0][1]}`;for(let i=0;i<P.length-1;i++){const p0=P[i-1]||P[i],p1=P[i],p2=P[i+1],p3=P[i+2]||p2;
  d+=` C${p1[0]+(p2[0]-p0[0])/6},${p1[1]+(p2[1]-p0[1])/6} ${p2[0]-(p3[0]-p1[0])/6},${p2[1]-(p3[1]-p1[1])/6} ${p2[0]},${p2[1]}`}return d}
function page(){document.body.insertAdjacentHTML('afterbegin','<div id="bgglow"></div><div id="brand">n<b>Ø</b>r<b>3</b>mors<b>3</b></div><div id="cap"></div><svg id="svg" class="layer" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')}
// subtitulos grandes: list = [[t, linea1, linea2], ...] ordenada
function caption(t,list){let c=list[0];for(const x of list)if(t>=x[0])c=x;const a=clamp((t-c[0])/.25);const e=$('cap');
  e.style.opacity=c[1]?a:0;e.style.transform=`translateY(${(1-out(a))*24}px)`;e.innerHTML=c[1]+(c[2]?'<br>'+c[2]:'')}
function ctaHTML(label,t0,t,tagHTML){const a=out(seg(t,t0,t0+.5)),p=1+.03*Math.sin((t-t0)*7);
  return `<div style="text-align:center"><div class="btn" style="opacity:${a};transform:scale(${(.85+.15*a)*p})">${label}</div><div class="tag" style="opacity:${seg(t,t0+.5,t0+1)}">${tagHTML}</div></div>`}
const C=window.CUES||[];            // [inicio, fin] de cada frase del guion (alineado con la voz)
const S=i=>C[i]?C[i][0]:0, E=i=>C[i]?C[i][1]:0;
window.addEventListener('DOMContentLoaded',()=>{page();if(window.init)window.init();window.render(0)});
