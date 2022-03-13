% clear all


% load particle data
load particle_path.mat
nx=length(x);
ny=length(y);
nt=length(time);
x_pos=reshape(particle(:,:,1),[nt*(nt+1),1]);
y_pos=reshape(particle(:,:,2),[nt*(nt+1),1]);

% plot depth
% clf
% contour(x,y,depth,'k')
% hold on
% plot(x_pos,y_pos,'bo')


% here were are going to plot the particle histograms of y-location of the particles,
%  throughout the domain (for various different x-locations).  This will
%  give us an idea of the size of the "particle plume"

num_bins=100;  % number of x-locations to create an individual histogram
bin_width=x(end-1)/num_bins;  % the x-width for each histogram, or the x-distance to sum all particles for each histogram
xbin=[bin_width/2:bin_width:x(end-1)];  % histogram center locations (in x)

% calculate each histogram
for i=1:num_bins
    xl=xbin(i)-bin_width/2;  % left x-boundary to count particles
    xr=xbin(i)+bin_width/2;  % right x-boundary to count particles
    bin_ind=find(x_pos>xl & x_pos<xr);  % indices in x_pos vector to include in this histogram
    
    x_c=x_pos(bin_ind);  % the x-postion of particles in this histogram
    y_c=y_pos(bin_ind);  % the y-position  of particles in this histogram
    clf
    histogram(y_c,100,'BinLimits',[y(1),y(end)])  % plot histogram for this location
    title(['Histogram of y-locations for particles between the x-bounds: ' num2str([xl xr])])
    xlabel('Y-location')
    ylabel('Particle Count')
    axis([y(1) y(end) 0 3000])
    view(90,90)
    mu(i)=mean(y_c);
    sigma(i)=std(y_c);
    pause(.1)

end

% plot the y-value mean and standard deviations of each histogram as a
% function of x
clf
plot(xbin,mu,xbin,mu+sigma,'b--',xbin,mu-sigma,'b--')
hold on
contour(x,y,depth,'k')
axis([x(1) x(end) y(1) y(end)])
legend('Mean Position of Plume','Standard Dev of Plume Width')
save particle_stats_full.mat xbin mu sigma x y depth













