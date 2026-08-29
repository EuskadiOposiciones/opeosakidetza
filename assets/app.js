
document.querySelectorAll('[data-play]').forEach(el=>{
  el.addEventListener('click',()=>{
    try{
      const key='opeosakidetza_play_clicks';
      const n=parseInt(localStorage.getItem(key)||'0',10);
      localStorage.setItem(key,String(n+1));
      localStorage.setItem('opeosakidetza_last_play_click',new Date().toISOString());
    }catch(e){}
  });
});
