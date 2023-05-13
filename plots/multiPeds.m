function [n] = multiPeds(t0,x0,y0,u0,v0,u1,u2,dt,alpha,beta,gamma,sigma_x,sigma_y,kappa,theta1,theta2,offset)

% Number of pedestrians
n = 100;

% Points for splines
x = [2, 4, 10, 15];
y = [15,18,22,26]; 

Bx = [2, 3, 2.5];
By = [0, 23, 26.25];
Cx = [2, 10, 15, 17];
Cy = [0, 4, 2.5, 4];
Dx = [2, 10, 14];
Dy = [0, 7.5, 17];
Ex = [2, 10, 20, 25, 27];
Ey = [0, 7.5, 6, 6.5, 26];

% values for spline
xx = linspace(2, 30, 100); 
pp = spline(x, y);
yy = ppval(pp, xx);

Bxx = linspace(2, 3, 100);
Bpp = spline(Bx, By);
Byy = ppval(Bpp, Bxx);

Cxx = linspace(2, max(Cx), 100);
Cpp = spline(Cx, Cy);
Cyy = ppval(Cpp, Cxx);

Dxx = linspace(2, max(Dx), 100);
Dpp = spline(Dx, Dy);
Dyy = ppval(Dpp, Dxx);

Exx = linspace(2, max(Ex), 100);
Epp = spline(Ex, Ey);
Eyy = ppval(Epp, Exx);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Create y_star mean path functions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

xx = linspace(2, 30, 100); 
pp = spline(x, y);
yy = ppval(pp, xx);

% Ystar for mean path 1
y_star = @(x) 25*ones(size(x)); 

% dYstar for mean path set up
d_pp = pp;
dy_coefs = [pp.coefs(:, 1)*3, pp.coefs(:, 2)*2, pp.coefs(:, 3)];
d_pp.coefs = dy_coefs;
d_pp.order = 3;

% dYstar for mean path
dy_star = @(x) ppval(d_pp, x);

% ddYstar for mean path set up
dd_pp = pp;
ddy_coefs = [d_pp.coefs(:, 1)*2, d_pp.coefs(:, 2)];
dd_pp.coefs = ddy_coefs;
dd_pp.order = 2;

% ddYstar for mean path
ddy_star = @(x) ppval(dd_pp, x);
%---------------------------------------------

% Ystar for mean path 4
Dy_star = @(Dx) ppval(Dpp,Dx);

% dYstar for mean path set up
d_Dpp = Dpp;
dDy_coefs = [Dpp.coefs(:,1)*3 Dpp.coefs(:,2)*2 Dpp.coefs(:,3)];
d_Dpp.coefs = dDy_coefs;
d_Dpp.order = 3;

% dYstar for mean path
dDy_star = @(Dx) ppval(d_Dpp,Dx);

% ddYstar for mean path set up
dd_Dpp = Dpp;
ddDy_coefs = [d_Dpp.coefs(:,1)*2 d_Dpp.coefs(:,2)];
dd_Dpp.coefs = ddDy_coefs;
dd_Dpp.order = 2;

% ddYstar for mean path
ddDy_star = @(Dx) ppval(dd_Dpp,Dx);

tinp = ceil(1.8/dt) + 1;

%need to make all demensions 2 to N peds into nan if not in space yet
%intial values for first ped, rest of peds, time step, and which ped has started
ti = 1;

l_b = 15;
u_b = 25;
% Generate a random y0
y0 = l_b + (u_b-l_b).*rand();

ped(1,1:5,1) = [t0, x0, y0,u0,v0];

ped(1,1:5,2:n) = NaN([1 5 (n-1)]);
startPed = 1;

%diffrent path options
pedpath = nan(n,1); %n pedestrians
pedpath(1,1) = 4*rand(1);
TimeLangth = n*30; % amount of time steps for each ped to enter the space search me

% Generate 5 random whole numbers in the range of 1 to 100
random_peds = randi([1, 100], [1, 10]);

writerObj = VideoWriter('C:\Users\lilin\OneDrive\Документы\CSULB Classes\MATH 479\Project\space_animation_old2'); % saved in .avi format
writerObj.FrameRate = 20; % Set the frame rate to n frames per second

open(writerObj);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculate pedestrian walk
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

while ti < TimeLangth

    for I = 1:n

        % choose random y0
        l_b = 15;
        u_b = 25;
        y0 = l_b + (u_b-l_b).*rand();

        % choose left or right starting x0
        value1 = 0;
        value2 = 70;
        random_number = rand;

        if random_number < 0.5
            x0 = value1;
        else
            x0 = value2;
            u0 = -u0;
        end

        % left trash cans
        if ped(ti,2,I) >= 20 && ped(ti,2,I) <= 23 && ped(ti,3,I) > 30
            ped(ti,4,I) = -1*ped(ti,4,I);
            ped(ti,5,I) = -1*ped(ti,5,I);
            y0 = 25;
        end

        % right trash cans
        if ped(ti,2,I) > 50 && ped(ti,2,I) <= 55 && ped(ti,3,I) > 30
            ped(ti,2,I) = ped(ti,2,I) + 0.9;
            ped(ti,4,I) = -1*ped(ti,4,I);
            ped(ti,5,I) = -1*ped(ti,5,I); % optional
            y0 = 25;
        end

        % upper boundry
        if ped(ti,3,I) >= 35 % y
            ped(ti,4,I) = -1*ped(ti,4,I);
            ped(ti,5,I) = -1*ped(ti,5,I);
        end


        % Check if I is in random_numbers using the "ismember" function
        if ismember(I, random_peds) && ped(ti,2,I) > 19 && ped(ti,2,I) < 59 % ismember(I, random_peds)
            y0 = 32;
        end

        y_star = @(x) y0*ones(size(x)); 
        By_star = @(Bx) y0*ones(size(Bx));
        Cy_star = @(Cx) ppval(Cpp,Cx);
        Dy_star = @(Dx) ppval(Dpp,Dx);
        Ey_star = @(Ex) ppval(Epp,Ex);

        if ti >= tinp
            tinp = ceil((ped(ti,1,I) + 1.8)/dt) + 1;
            ped(ti,1:5,startPed + 1) = [ped(ti,1,startPed),x0,y0,u0,v0]; % add next ped
            ped(ti,1:5,startPed + 1)
            startPed = startPed + 1; % add next
            pedpath(startPed,1) = 4*rand(1); % create random number for ped path
        end


        % mean path 1
        if pedpath(I,1) > 0 && pedpath(I,1) <= 1
            normalV = [dy_star(ped(ti,2,I)), -1]./sqrt(1 + dy_star(ped(ti,2,I)).^2);
            rho = abs(((1 + dy_star(ped(ti,2,I)).^2).^1.5)./ddy_star(ped(ti,2,I)));
            centripetalF = normalV.*(ped(ti,4,I).^2 + ped(ti,5,I).^2)/rho;

            ped(ti+1,1,I) = ped(ti,1,I) + dt;% update time
            ped(ti+1,2,I) = ped(ti,2,I) + ped(ti,4,I)*dt;% update Ped1 X
            ped(ti+1,4,I) = ped(ti,4,I) - alpha(1)*ped(ti,4,I)*(ped(ti,4,I)-u1)*(ped(ti,4,I)-u2)*dt + sigma_x(1)*(randn(1)*sqrt(dt)) + centripetalF(1)*dt;% update Ped1 U
            ped(ti+1,3,I) = ped(ti,3,I) + ped(ti,5,I)*dt;% update Ped1 Y
            ped(ti+1,5,I) = ped(ti,5,I) - beta(1)*(ped(ti,3,I) - y_star(ped(ti,2,I)))*dt - gamma(1)*ped(ti,5,I)*dt + sigma_y(1)*(randn(1)*sqrt(dt)) + centripetalF(2)*dt;% update Ped1 V
        end

        % mean path 2: DOWN
        if pedpath(I,1) > 1 && pedpath(I,1) <= 2
            normalV = [dy_star(ped(ti,2,I)), -1]./sqrt(1 + dy_star(ped(ti,2,I)).^2);
            rho = abs(((1 + dy_star(ped(ti,2,I)).^2).^1.5)./ddy_star(ped(ti,2,I)));
            centripetalF = normalV.*(ped(ti,4,I).^2 + ped(ti,5,I).^2)/rho;
            
            ped(ti+1,1,I) = ped(ti,1,I) + dt;% update time
            ped(ti+1,2,I) = ped(ti,2,I) + ped(ti,4,I)*dt; % update Ped1 X
            ped(ti+1,4,I) = ped(ti,4,I) - alpha(1)*ped(ti,4,I)*(ped(ti,4,I)-u1)*(ped(ti,4,I)-u2)*dt + sigma_x(1)*(randn(1)*sqrt(dt)) + centripetalF(1)*dt;% update Ped1 U
            
            if (ped(ti,2,I) > 27 && ped(ti,2,I) < 43)
                % going down
                ped(ti+1,3,I) = ped(ti,3,I) - ped(ti,5,I)*dt/2; % y
            else
                ped(ti+1,3,I) = ped(ti,3,I) + ped(ti,5,I)*dt;% update Ped1 Y
            end
            ped(ti+1,5,I) = ped(ti,5,I) - beta(1)*(ped(ti,3,I) - y_star(ped(ti,2,I)))*dt - gamma(1)*ped(ti,5,I)*dt + sigma_y(1)*(randn(1)*sqrt(dt)) + centripetalF(2)*dt;% update Ped1 V
        end

        % mean path 3: UP
        if pedpath(I,1) > 2 && pedpath(I,1) <= 3
            normalV = [dy_star(ped(ti,2,I)), -1]./sqrt(1 + dy_star(ped(ti,2,I)).^2);
            rho = abs(((1 + dy_star(ped(ti,2,I)).^2).^1.5)./ddy_star(ped(ti,2,I)));
            centripetalF = normalV.*(ped(ti,4,I).^2 + ped(ti,5,I).^2)/rho;
            
            ped(ti+1,1,I) = ped(ti,1,I) + dt;% update time
            ped(ti+1,2,I) = ped(ti,2,I) + ped(ti,4,I)*dt; % update Ped1 X
            ped(ti+1,4,I) = ped(ti,4,I) - alpha(1)*ped(ti,4,I)*(ped(ti,4,I)-u1)*(ped(ti,4,I)-u2)*dt + sigma_x(1)*(randn(1)*sqrt(dt)) + centripetalF(1)*dt;% update Ped1 U
            
            if (ped(ti,2,I) > 32 && ped(ti,2,I) < 40)
                % going up
                ped(ti+1,3,I) = ped(ti,3,I) + 0.24*dt + 0.01;% update Ped1 Y
            else
                ped(ti+1,3,I) = ped(ti,3,I) + ped(ti,5,I)*dt;% update Ped1 Y
            end
            
            ped(ti+1,5,I) = ped(ti,5,I) - beta(1)*(ped(ti,3,I) - y_star(ped(ti,2,I)))*dt - gamma(1)*ped(ti,5,I)*dt + sigma_y(1)*(randn(1)*sqrt(dt)) + centripetalF(2)*dt;% update Ped1 V
        end

        % mean path 4 spline
        if pedpath(I,1) > 3 && pedpath(I,1) <= 4
            normalV = [dDy_star(ped(ti,2,I)), -1]./sqrt(1 + dDy_star(ped(ti,2,I)).^2);
            rho = abs(((1 + dDy_star(ped(ti,2,I)).^2).^1.5)./ddDy_star(ped(ti,2,I)));
            centripetalF = normalV.*(ped(ti,4,I).^2 + ped(ti,5,I).^2)/rho;

            ped(ti+1,1,I) = ped(ti,1,I) + dt;% update time
            ped(ti+1,2,I) = ped(ti,2,I) + ped(ti,4,I)*dt;% update Ped1 X
            ped(ti+1,4,I) = ped(ti,4,I) - alpha(1)*ped(ti,4,I)*(ped(ti,4,I)-u1)*(ped(ti,4,I)-u2)*dt + sigma_x(1)*(randn(1)*sqrt(dt)) + centripetalF(1)*dt;% update Ped1 U
            ped(ti+1,3,I) = ped(ti,3,I) + ped(ti,5,I)*dt;% update Ped1 Y
            ped(ti+1,5,I) = ped(ti,5,I) - beta(1)*(ped(ti,3,I)-Dy_star(ped(ti,2,I)))*dt - gamma(1)*ped(ti,5,I)*dt + sigma_y(1)*(randn(1)*sqrt(dt)) + centripetalF(2)*dt;% update Ped1 V
        end

        normalV = [dy_star(ped(ti,2,I)), -1]./sqrt(1 + dy_star(ped(ti,2,I)).^2);
        rho = abs(((1 + dy_star(ped(ti,2,I)).^2).^1.5)./ddy_star(ped(ti,2,I)));
        centripetalF = normalV.*(ped(ti,4,I).^2 + ped(ti,5,I).^2)/rho;
                     
        ped(ti+1,1,I) = ped(ti,1,I) + dt;% update time
        ped(ti+1,2,I) = ped(ti,2,I) + ped(ti,4,I)*dt; % update Ped1 X
        ped(ti+1,4,I) = ped(ti,4,I) - alpha(1)*ped(ti,4,I)*(ped(ti,4,I)-u1)*(ped(ti,4,I)-u2)*dt + sigma_x(1)*(randn(1)*sqrt(dt)) + centripetalF(1)*dt;% update Ped1 U
        ped(ti+1,3,I) = ped(ti,3,I) + ped(ti,5,I)*dt;% update Ped1 Y

        % going DOWN
        if (ped(ti,2,I) > 27 && ped(ti,2,I) < 43) && (pedpath(I,1) > 1 && pedpath(I,1) <= 2)
            ped(ti+1,3,I) = ped(ti,3,I) - ped(ti,5,I)*dt/2; % y

        end
        % going UP
        if (ped(ti,2,I) > 32 && ped(ti,2,I) < 40) && (pedpath(I,1) > 2 && pedpath(I,1) <= 3)
            ped(ti+1,3,I) = ped(ti,3,I) + 0.24*dt + 0.01;% update Ped1 Y
        end

        ped(ti+1,5,I) = ped(ti,5,I) - beta(1)*(ped(ti,3,I)-y_star(ped(ti,2,I)))*dt - gamma(1)*ped(ti,5,I)*dt + sigma_y(1)*(randn(1)*sqrt(dt)) + centripetalF(2)*dt;% update Ped1 V

    end
    ti = ti+1;
end

ti = 1;

% Start the timer
tic;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% while loop for ploting pedestrians
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

while ti < TimeLangth
    % deleting pedestrians heading out of bounds
    for I = 1:n
        if ped(ti,2,I) < 0 || ped(ti,2,I) > 70 % x
            ped(ti,1:5,I) = NaN([1 5]);
        end
        if ped(ti,3,I) < 0 || ped(ti,3,I) > 35 % y
            ped(ti,1:5,I) = NaN([1 5]);
        end

        % entering bookstore
        if ped(ti,3,I) > 32 && ped(ti,3,I) < Inf % y
            if ped(ti,2,I) > 30 && ped(ti,2,I) < 40 % x
                ped(ti,1:5,I) = NaN([1 5]);
            end
        end

        % left tent
        if ped(ti,3,I) <= 12 && (ped(ti,2,I) > 5 && ped(ti,2,I) < 28) % y
            ped(ti,1:5,I) = NaN([1 5]);
        end

        % right tent
        if ped(ti,3,I) <= 12 && (ped(ti,2,I) > 42 && ped(ti,2,I) < 67) % y
            ped(ti,1:5,I) = NaN([1 5]);
        end

    end

    [i] = corridor(x0,y0);

    hold on
    plot(squeeze(ped(ti,2,:)),squeeze(ped(ti,3,:)),'r.','MarkerSize',15);
    
    drawnow

    writeVideo(writerObj, getframe(gcf)); % get the current figure and add it to the video

    ti = ti + 1;

end
close(writerObj);

% Stop the timer and print the elapsed time
elapsed_time = toc;
fprintf('Elapsed time: %f seconds\n', elapsed_time);

end
