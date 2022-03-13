% clear all

% this script will calculate the path of a constant stream of particles
% released from the left boundary of the domain.   If you just want to see
% an animation of the output, use reload=0 below.  If you wish to
% recalculate the entire particle trajectories, use reload=1.
reload=1;

if reload==1
    load ENE512_prob2.mat
    % contains the following variables:
    % x - the x-position vector, length nx
    % y - the y-position vector, length ny
    % time - the time vector, length nt
    % depth - the river depth surface, size ny by nx
    % u - the x-component of velocity, size ny by nx by nt
    % v - the y-component of velocity, size ny by nx by nt
    
    nx=length(x);
    ny=length(y);
    nt=length(time);
    
    % Particle tracking
    particle=zeros(nt,nt,2);  % nt particles, storing x,y position at all nt times
    % initial position of all particles
    particle(:,:,1)=0; % initial x-position
    particle(:,:,2)=y(end)/2; % initial y-position
    
    dt=time(2)-time(1); % constant dt
    figure(3)
    for n=1:nt
        [n,nt];
        clf
        contour(x,y,depth,'k');
        hold on
        for p=1:n
            xc=particle(p,n,1);
            if xc<x(end)  % particle hasnt left domain
                yc=particle(p,n,2);
                xi=find(x>=xc,1);
                yi=find(y>=yc,1);
                uc=u(yi,xi,n);
                vc=v(yi,xi,n);
                particle(p,n+1,1)=particle(p,n,1)+uc*dt;
                particle(p,n+1,2)=particle(p,n,2)+vc*dt;
            else  % particle has left domain, hold position where it left
                particle(p,n+1,1)=x(end);
                particle(p,n+1,2)=particle(p,n,2);
            end
            
            plot(xc,yc,'bo')
        end
    end
    
    save particle_path.mat particle x y time depth
    
else
    load particle_path
    nx=length(x);
    ny=length(y);
    nt=length(time);
    for n=1:nt
        [n,nt];
        clf
        contour(x,y,depth,'k')
        hold on
        xc=squeeze(particle(:,n,1));
        yc=squeeze(particle(:,n,2));
        plot(xc,yc,'bo')
        %pause(0.01)
    end
end
