var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
ctx.font="30px Arial";

ctx.fillStyle = "#d5dbdb";
ctx.fillRect(0,0,450,450);
ctx.strokeRect(0,0,450,450);
//draw vertical lines
for (i=1; i <= 8; i++)
{
        ctx.moveTo(i*50,0);
        ctx.lineTo(i*50, 450);
        ctx.stroke();
}
//draw horizontal lines
for (i=1; i<=8; i++)
{
        ctx.moveTo(0, i*50);
        ctx.lineTo(450, i*50);
        ctx.stroke();
}
var coordenadas = []
ctx.canvas.addEventListener('click', function(event){
        var rect = canvas.getBoundingClientRect();
        var mouseX = event.clientX - rect.left;
        var mouseY = event.clientY - rect.top;
        var col = Math.round(mouseX/50);
        var bit = Math.round(mouseY/50);
        ctx.fillStyle = "#5A6A62";
        if ((col >=1 & col <= 8) & (bit >=1 & bit <= 8))
        {
                ctx.fillRect((Math.round(mouseX/50)*50)-10,(Math.round(mouseY/50)*50)-10,20,20);
                coordenadas.push(col);
                coordenadas.push(bit);
        }

});
var limpar = document.getElementById("clean");
limpar.addEventListener('click', function(event){
        ctx.fillStyle = "#d5dbdb";
        ctx.fillRect(0,0,450,450);
        ctx.strokeRect(0,0,450,450);
        for (i=1; i <= 8; i++)
        {
                ctx.moveTo(i*50,0);
                ctx.lineTo(i*50, 450);
                ctx.stroke();
        }
        //draw horizontal lines
        for (i=1; i<=8; i++)
        {
                ctx.moveTo(0, i*50);
                ctx.lineTo(450, i*50);
                ctx.stroke();
        }
        coordenadas = [];
});
var bot_enviar = document.getElementById("submit");
bot_enviar.addEventListener('click', function(event){

        var connector_name = document.getElementById("nome-conector").value;
        console.log(coordenadas);
        $.ajax({
                type: "POST",
                url: "/add_conn_scheema",
                data: {c: JSON.stringify(coordenadas),
                        name: connector_name}
        }).done(function(o) {
                console.log('saved');
                alert("Conector Salvo");
        });
});
