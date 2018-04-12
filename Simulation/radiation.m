function [ vecx, vecy ] = radiation( rad )
%RADIATION Summary of this function goes here
%   Detailed explanation goes here
theta = linspace(0,2*pi);
vecx = rad*cos(theta);
vecy = rad*sin(theta);

end

