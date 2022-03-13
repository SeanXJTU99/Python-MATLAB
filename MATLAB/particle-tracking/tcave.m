function particle = tcave(ubar,vbar,Dx,Dy,x,y,time,~)
%UNTITLED3 此处显示有关此函数的摘要
%   此处显示详细说明

nt=length(time);
particle=zeros(nt,nt,2);
particle(:,:,1)=0; % initial x-position
particle(:,:,2)=y(end)/2; % initial y-position
dt=time(2)-time(1);

for n=1:nt
%     clf
%     contour(x,y,depth,'k')
%     hold on
    for p=1:n
        xc=particle(p,n,1);
        if xc<x(end)  % particle hasnt left domain
            %yc=particle(p,n,2);
            xi=find(x>=xc,1);
            particle(p,n+1,1)=particle(p,n,1)+ubar(xi)*dt+sqrt(Dx(xi)*dt)*(rand(1)*2-1);
            particle(p,n+1,2)=particle(p,n,2)+vbar(xi)*dt+sqrt(Dy*dt)*(rand(1)*2-1);
        else  % particle has left domain, hold position where it left
            particle(p,n+1,1)=x(end);
            particle(p,n+1,2)=particle(p,n,2);
        end
        %plot(xc,yc,'bo');
    end
    %pause(0.01);
end
end

