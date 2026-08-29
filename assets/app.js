
document.querySelectorAll('a[data-play]').forEach(a=>{
  a.addEventListener('click',()=>{ try{localStorage.setItem('lastPlayClick',Date.now().toString())}catch(e){} });
});
