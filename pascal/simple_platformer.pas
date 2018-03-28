program platformer;
uses graphabc, events;
var x,y,x_speed,y_speed,grav,rings,ring_x,ring_y:integer; str_rings, room:string;

procedure KeyDown(Key: integer);
begin
     case Key of
          VK_Left: x_speed:=-5;
          VK_Right: x_speed:=5;
          VK_Space: if y = 300 then y_speed:=-15;
          VK_Return: if room = 'title' then room:='main';
     end;
end;

procedure KeyUp(Key: integer);
begin
     case Key of
          VK_Left: x_speed:=0;
          VK_Right: x_speed:=0;
     end;
end;

begin
     OnKeyDown:=KeyDown;
     OnKeyUp:=KeyUp;
     grav:=1;
     x_speed:=0;
     y_speed:=0;
     x:=200;
     y:=300;
     rings:=0;
     ring_x:=random(290)+5;
     ring_y:=random(90)+200;
     room:='title';
     
     SetWindowWidth(500);
     SetWindowHeight(400);
     
     while true do
     begin
          if room = 'title' then
          begin
               redraw();
               lockdrawing();
               TextOut(200,150,'A simple platformer.');
               TextOut(200,175,'Press Enter to start.');
               TextOut(150,200,'Use arrows to move. Press space to jump.');
               TextOut(205,225,'Collect all rings!');
               TextOut(200,275,'Made by OSA413.');
               TextOut(215,300,'18.04.2017');
          end
          else if room = 'main' then
               begin
               x:=x+x_speed;
               y:=y+y_speed;
               if y_speed < 10 then
               begin
                    y_speed:=y_speed + grav;
               end;
               if y >=300 then
               begin
                    y:=300;
               end;
               if x <=10 then
               begin
                    x:=10;
               end;
               if x >=490 then
               begin
                    x:=490;
               end;
               if (x+10 > ring_x-5) and (x-10 < ring_x+5) and (y > ring_y-5) and (y-20 < ring_y+5) then
               begin
                    ring_x:=random(290)+5;
                    ring_y:=random(90)+200;
                    rings:=rings+1;
               end;

               ///Draw event
               redraw();
               lockdrawing();
               floodfill(0,0,clBlack);
               setbrushcolor(clskyblue);
               rectangle(0,0,500,400);
               setbrushcolor(clbrown);
               rectangle(0,300,500,400);
               setbrushcolor(clgreen);
               rectangle(0,300,500,310);
               setbrushcolor(clwhite);
               rectangle(x-10,y,x+10,y-20);
               setbrushcolor(clyellow);
               circle(ring_x,ring_y,5);
          
               SetFontColor(clblack);
               str(rings,str_rings);
               setbrushcolor(clskyblue);
               TextOut(10,10,'Rings: '+str_rings);
          end;
     end;
end.
          