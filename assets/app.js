// OPE Osakidetza — utilidades locales. Sin almacenamiento en navegador.
(function(){
  'use strict';
  var form=document.getElementById('study-planner');
  if(!form) return;
  var category=document.getElementById('planner-category');
  var total=document.getElementById('planner-total');
  var days=document.getElementById('planner-days');
  var rounds=document.getElementById('planner-rounds');
  var result=document.getElementById('planner-result');

  category.addEventListener('change',function(){
    var opt=category.options[category.selectedIndex];
    var preset=parseInt(opt.getAttribute('data-total')||'',10);
    if(preset>0) total.value=preset;
  });

  form.addEventListener('submit',function(ev){
    ev.preventDefault();
    var q=Math.max(1,parseInt(total.value||'0',10));
    var d=Math.max(1,parseInt(days.value||'0',10));
    var r=Math.max(1,parseInt(rounds.value||'0',10));
    var exposures=q*r;
    var daily=Math.ceil(exposures/d);
    var first=Math.ceil(q/d);
    var cat=category.value||'manual';
    result.innerHTML='<span class="planner-kicker">Ritmo medio estimado</span>'+
      '<strong class="planner-big">'+daily+' preguntas/día</strong>'+
      '<p>'+q+' preguntas × '+r+' vueltas ÷ '+d+' días = '+exposures.toLocaleString('es-ES')+' exposiciones planificadas. Una sola cobertura equivaldría a unas '+first+' preguntas/día.</p>'+
      '<div class="planner-phases"><div><b>1ª capa</b><span>100% de cobertura</span></div><div><b>2ª capa</b><span>prioriza fallos + dudas</span></div><div><b>Final</b><span>mezcla y simula</span></div></div>';
    document.dispatchEvent(new CustomEvent('ope:studyplan',{detail:{category:cat,questions_total:q,days_until_exam:d,full_rounds:r,questions_per_day:daily}}));
  });
})();
