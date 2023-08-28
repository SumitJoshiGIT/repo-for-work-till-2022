let Game=
{
    dice:1,
    turn:1,
    hold_button:document.querySelector('#hold'),
    new_game_button:document.querySelector('#new_game'),
    roll_button:document.querySelector('#Roll'),
    scoring_function:function(n){return Math.round(0.2*(this["player"+n].score+1)%10+0.5*this.dice);},
   
    player1:{
            obj:document.querySelector('#Player1'),
            score:0,
            hold:0,
            score_:document.querySelector('#V1'),
            hold_:document.querySelector('#V2')
   },
   
   player2:{
    obj:document.querySelector('#Player2'),
    score:0,
    hold:0,
    score_:document.querySelector('#V3'),
    hold_:document.querySelector('#V4')
}
,
   update:function(n,hold=this["player"+n].hold,score=this["player"+n].score){ 
      console.log(hold,score)
      this["player"+n].hold=hold;
      this["player"+n].score=score;
      this["player"+n].hold_.textContent=hold;
      this["player"+n].score_.textContent=score; 
   }
   ,
   new_game:function(){
      this.update(1,0,0);
      this.update(2,0,0);      
   },

   hold:function(){
      this.update(this.turn,hold=this["player"+this.turn].hold+this["player"+this.turn].score,score=0);},
   
   roll:function(){
    this.dice=Math.floor((Math.random())*6)+1;
    if (this["player"+this.turn].hold>=100){console.log("player"+this.turn+"wins");}
    else if (this.dice==1){
          this.change();
    }
    else{
            this["player"+this.turn].score+=this.scoring_function(this.turn);
            this.update(this.turn) ;
         }}
   ,
   start:function(){
      this.hold_button.addEventListener('click',()=>this.hold());
      this.new_game_button.addEventListener('click',()=>this.new_game());
      this.roll_button.addEventListener('click',()=>this.roll());
      this.player1.obj.style.opacity=0.5;
      this.player2.obj.style.opacity=0.4;
      this.update(1,0,7);
      this.update(2,0,7);

   },
   change:function(){
     if (this.turn===1){
        this.update(1,hold=this.player1.hold,score=0);
        this.turn=2;
        this.player1.obj.style.opacity=0.4;
        this.player2.obj.style.opacity=0.5;
    }
     else{
        this.update(2,hold=this.player2.hold,score=0);
        this.turn=1;
        this.player2.obj.style.opacity=0.4;
        this.player1.obj.style.opacity=0.5;
      }
   }
}
console.log("Start")
Game.start();
console.log("Game")

