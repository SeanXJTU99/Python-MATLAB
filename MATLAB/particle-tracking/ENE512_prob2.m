clear all

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

% EXAMPLE plot a time series of the data
x_ts=50; % x-location of time series
y_ts=5; % y-location of time series

u_ts=squeeze(interp3(x,y,time,u,x_ts,y_ts,time)); % interpolates the entire u surface time stack at the locations x_ts and y_ts
% Note that the "squeeze" function eliminates dimensions of 1 in a matrix,
% so a matrix of size 1 by 1 by nt will have size nt after the squeeze operation
v_ts=squeeze(interp3(x,y,time,v,x_ts,y_ts,time)); % interpolates the entire v surface time stack at the locations x_ts and y_ts
% You can use this interp3 function to find the u and v values at any
% arbitrary location and time.  For example, if you wanted to find the u
% component at x_c=80, y_c=12, time_c=200, you could call
% "u_c=squeeze(interp3(x,y,time,u,x_c,y_c,time_c))" and you would get the
% value of u at that location and time.

figure(1)
clf
hold on
plot(time,u_ts)
plot(time,v_ts)
xlabel('Time (Seconds)')
ylabel('Velocity (m/s)')
legend('U-component','V-component')
title(['Time Series of Velocity Components at (x,y) = (' num2str(x_ts) ',' num2str(y_ts) ')' ])


% EXAMPLE plot an animation of the velocity components
figure(2)
for n=1:nt
    clf
    subplot(2,1,1)
    pcolor(x,y,u(:,:,n))
    shading interp
    hold on
    contour(x,y,depth,'w')
    caxis([-0.5 0.5])
    colorbar
    xlabel('X (m)')
    ylabel('Y (m)')
    title(['U-Component of Velocity (m/s) at Time (sec) = ' num2str(time(n))])
    
    subplot(2,1,2)
    pcolor(x,y,v(:,:,n))
    shading interp
    hold on
    contour(x,y,depth,'w')
    caxis([-0.5 0.5])
    colorbar
    xlabel('X (m)')
    ylabel('Y (m)')
    title(['V-Component of Velocity (m/s) at Time (sec) = ' num2str(time(n))])
    
    pause(.1)
end

% EXAMPLE plot an animation of the velocity vectors
figure(3)
for n=1:nt
    clf
    quiver(x,y,u(:,:,n),v(:,:,n))
    hold on
    contour(x,y,depth,'w')
    colorbar
    xlabel('X (m)')
    ylabel('Y (m)')
    title(['Velocity Vectors at Time (sec) = ' num2str(time(n))])
 
    pause(.1)
end


% EXAMPLE plot an animation of the vertical vorticity
figure(4)
for n=1:nt
    clf
    dudy=zeros(ny,nx);
    dvdx=zeros(ny,nx);
    for i=2:nx-1
        for j=2:ny-1
            dudy(j,i)=( u(j+1,i,n) - u(j-1,i,n) )/ (y(j+1)-y(j-1));
            dvdx(j,i)=( v(j,i+1,n) - v(j,i-1,n) )/ (x(i+1)-x(i-1));
        end
    end
    vort=dudy-dvdx;
    
    pcolor(x,y,vort)
    shading interp
    hold on
    contour(x,y,depth,'w')
    caxis([-0.1 0.1])
    colorbar
    xlabel('X (m)')
    ylabel('Y (m)')
    title(['Vertical Vorticity at Time (sec) = ' num2str(time(n))])
 
    pause(.1)
end

















