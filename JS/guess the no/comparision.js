'use strict';
let val;
let score=0;
let High_s=0;
let num=7;
let m_val=0

let task1=function(){
    val=Number(document.querySelector('#i1').value);
    document.querySelector('#i1').value=null;
    if (m_val==0){
    if (val===num){
        score+=1;   
        document.querySelector('#Sp1').textContent=String(score)
        document.querySelector('#H').textContent="Correct Answer!";
        document.querySelector('#sub_1').style.backgroundColor='#60b347';
        m_val=1;
          }
    else{
        
        if (score>High_s){document.querySelector('#Sp2').textContent=String(score);High_s=score;}
        score=0;
        document.querySelector('#Sp1').textContent=score;
        document.querySelector('#H').textContent="Guess Again?";    
        document.querySelector('#sub_1').style.backgroundColor='#ff1a1a';
        
    }      
    document.querySelector('#B1').style.display='none';
    document.querySelector('input').style.display='none';
  
    
}
        
}
let task2=function(){
     
     m_val=0;
     document.querySelector('#H').textContent="What is your guess?";    
     document.querySelector('#sub_1').style.backgroundColor='#131516';
     document.querySelector('#B1').style.display='inline';
     document.querySelector('input').style.display='inline';
    


}
document.querySelector('#B1').addEventListener('click',task1)
document.querySelector('#B2').addEventListener('click',task2)



