function [ distances ] = distance( rssi )
%DISTANCE Summary of this function goes here
%   Detailed explanation goes here
distances = [];
for i = 1:length(rssi)
    distances(i) = 10.^((-rssi(i)+47)/20);
end
end

