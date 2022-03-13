
tspan = 0:0.01:10;

xmax = 2;
xmin = 0;
ymax = 2;
ymin = 0;

% This defines and labels the axes of the phase portrait
axis([xmin xmax ymin ymax]);
     xlabel('x','FontSize',20);
     ylabel('y','FontSize',20);
hold on


npoints = 20;

for i=0:npoints
    x0 = xmin + i*(xmax-xmin)/npoints;
    for j=0:npoints
            y0 = ymin + j*(ymax-ymin)/npoints;
            [t,y] = ode15s(@logs,tspan,[x0;y0]);
            plot(y(:,1),y(:,2));
    end
end




