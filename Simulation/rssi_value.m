function [ rssi ] = rssi_value( rad )
%RSSI_VALUE Summary of this function goes here
%   Detailed explanation goes here
rssi = -(20*log10(rad)-36);%-rand()*0.1);

end

