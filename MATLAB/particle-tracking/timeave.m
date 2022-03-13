function particle = timeave(umean,vmean,Dx,Dy,x,y,time)
%UNTITLED2 此处显示有关此函数的摘要
%   此处显示详细说明
nt=length(time);
particle=zeros(nt,nt,2);
particle(:,:,1)=0;
particle(:,:,2)=y(end)/2;
dt=time(2)-time(1);
for n=1:nt
%     clf;
%     contour(x,y,depth);
%     hold on;
    for p=1:n
        xc=particle(p,n,1);
        if xc<x(end)  % particle hasnt left domain
            yc=particle(p,n,2);
            xi=find(x>=xc,1);
            yi=find(y>=yc,1);
            particle(p,n+1,1)=particle(p,n,1)+umean(yi,xi)*dt+sqrt(Dx(yi,xi)*dt)*(rand(1)*2-1);
            particle(p,n+1,2)=particle(p,n,2)+vmean(yi,xi)*dt+(Dy(yi,xi)*sqrt(dt))*(rand(1)*2-1);
        else  % particle has left domain, hold position where it left
            particle(p,n+1,1)=x(end);
            particle(p,n+1,2)=particle(p,n,2);
        end
%          plot(xc,yc,'bo');
    end
%     pause(0.01);
end
% figure(6);
% contour(x,y,depth,'k');
% hold on
% title('time-averaged')
% nt=length(time);
%     for p=1:nt
%         xc=particle(p,nt,1);
%         yc=particle(p,nt,2);
%         plot(xc,yc,'bo');
%     end
end

