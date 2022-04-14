#!/usr/bin/env python3
# coding: utf-8


from dvc_input import DVC_Parameters, DVC_Model, DVC_H5_Writer


# create the parameters

param = DVC_Parameters(analysis='correlation', 
                        ref_im='ref_im.raw',
                        def_im='def_im.raw', 
                        res_file='out.res', 
                        roi=[0, -1, 0, -1, 0, -1],
                        pixel_size=1.0,
                        restart=0,
                        convergence_limit=1.0e-4,
                        iter_max=30, 
                        regularization_param=16,
                        regularization_type='tiko',
                        psample=1,
                        image_size=[])


# create the model variables

model = DVC_Model(basis='fem',
                  nscale=3,
                  mesh_size=[16, 16, 16])

# print the parameters and model variables on the console

print(param)

print(model)

# the parameters can be accessed and changed using the dot notation after the creation of the objects

# print('Initial analysis type \n')
# print(f'Analysis: {param.analysis}')

# param.analysis = 'carrot_cake_rules'
# print('')
# print('New analysis type \n')
# print(f'Analysis: {param.analysis}')

# initialize the writer object receiving the previously created objects

writer = DVC_H5_Writer(parameters=param, 
                        model = model,
                        h5filename='/data/visitor/ihma244/id11/DVC_Analysis/DVC_Settings.h5')

# write the H5 file on disk

writer.write_h5file()