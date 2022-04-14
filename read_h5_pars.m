function [param, model] = read_h5_pars(filename)
param = struct();
model = struct();

param.analysis = string(h5read(filename, '/param/analysis'));
param.reference_image = string(h5read(filename, '/param/reference_image'));
param.deformed_image = string(h5read(filename, '/param/deformed_image'));
param.result_file = string(h5read(filename, '/param/result_file'));
param.roi = [h5read(filename, '/param/roi')'];
param.pixel_size = h5read(filename, '/param/pixel_size');
param.restart = h5read(filename, '/param/restart');
param.conv_lim = h5read(filename, '/param/conv_lim');
param.iter_max = h5read(filename, '/param/iter_max');
param.regularization_type = string(h5read(filename, '/param/regularization_type'));
param.regularization_param = (h5read(filename, '/param/regularization_param'));
param.psample = h5read(filename, '/param/psample');

model.basis = string(h5read(filename, '/model/basis'));
model.nscale = h5read(filename, '/model/nscale');
model.mesh_size = h5read(filename, '/model/mesh_size')';

end