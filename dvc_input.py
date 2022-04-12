#!/usr/bin/env python3
# coding: utf-8


from dataclasses import dataclass
import h5py
import os
       
@dataclass
class DVC_Parameters:
    def __init__(self, 
                analysis:str = 'correlation', 
                ref_im:str = 'ref_im.raw', 
                def_im:str = 'def_im.raw',
                res_file:str = 'out.res', 
                roi:list = [0, -1, 0, -1, 0, -1], 
                pixel_size:float = 1.0,
                restart:int =0,
                convergence_limit:float = 1.0e-4, 
                iter_max:int = 30,
                regularization_type:str = 'tiko', 
                regularization_param:int =16, 
                psample:int = 1,
                image_size:list = []):

        self.analysis = analysis
        self.reference_image = ref_im
        self.deformed_image = def_im
        self.result_file = res_file
        self.roi = roi
        self.pixel_size = pixel_size
        self.restart = restart
        self.conv_lim = convergence_limit
        self.iter_max = iter_max
        self.regularization_type = regularization_type
        self.regularization_param = regularization_param
        self.psample = psample

        if self.reference_image.split('.')[-1] == 'raw':
            if image_size == ():
                print(Warning('You will need the size of the raw images to run DVC!!'))
            
            self.image_size = image_size

    def __str__(self):
        string = ("-------------PARAMETERS--------------- \n"+
        f"Analysis: {self.analysis} \n" +
        f"Reference image: {self.reference_image} \n" + 
        f"Deformed image: {self.deformed_image} \n" +
        f"Result file: {self.result_file} \n" +
        f"ROI: {self.roi} \n" +
        f"Pixel size: {self.pixel_size} \n" +
        f"Restart: {self.restart} \n" +
        f"Convergence limit: {self.conv_lim} \n" +
        f"Maximum iterations: {self.iter_max} \n" +
        f"Regularization type: {self.regularization_type} \n" +
        f"Regularization parameter: {self.regularization_param} \n" +
        f"Pixel skip: {self.psample} \n \n") 
        return string

@dataclass
class DVC_Model:
    def __init__(self,
                basis:str = 'fem',
                nscale:int = 3,
                mesh_size:tuple = (16, 16, 16)):

        self.basis = basis
        self.nscale = nscale
        self.mesh_size = mesh_size

    def __str__(self):

        string = ("----------------MODEL----------------- \n"+
                 f'Basis function: {self.basis} \n' +
                 f'Coarse graining scales: {self.nscale} \n' +
                 f'Mesh size: {self.mesh_size} \n \n')
        return string

class DVC_H5_Writer(DVC_Parameters, DVC_Model):
    def __init__(self,
                parameters:DVC_Parameters = DVC_Parameters(),
                model:DVC_Model = DVC_Model(),
                h5filename:str = './DVC_Settings.h5'):
        super().__init__(self)
        # defining the h5 file path
        self.filename = h5filename

        # defining the parameters values
        self.analysis =parameters.analysis
        self.reference_image =parameters.reference_image
        self.deformed_image =parameters.deformed_image
        self.result_file =parameters.result_file
        self.roi =parameters.roi
        self.pixel_size =parameters.pixel_size
        self.restart =parameters.restart
        self.conv_lim =parameters.conv_lim
        self.iter_max =parameters.iter_max
        self.regularization_type =parameters.regularization_type
        self.regularization_param =parameters.regularization_param
        self.psample =parameters.psample

        # defining the model variables
        self.basis = model.basis
        self.nscale = model.nscale
        self.mesh_size = model.mesh_size    

    def write_h5file(self):

        if os.path.exists(self.filename):

            answer = input('There is a file with the name you asked for. Do you want to overwrite it? (y/n)').lower()
            
            if answer == 'y':
                with h5py.File(name=self.filename, mode='w') as h5file:
                    h5file.create_group(name='/param')
                    h5file.create_group(name='/model')

                    # h5file['/param/analysis'] = self.analysis
                    # h5file['/param/reference_image'] = self.reference_image

                    h5file.create_dataset(name='/param/analysis', data=self.analysis)
                    h5file.create_dataset(name='/model/basis', data=self.basis)

                    # h5file['/model/basis'] = self.basis
        
   












        
        

    

if __name__ == '__main__':

    param = DVC_Parameters(analysis='pedro')
    model = DVC_Model()
    # writer = DVC_H5_Writer(param, model).write_h5file(param, model)
    writer = DVC_H5_Writer()


    print(param)
    print(model)
    print()
    print(writer.__dict__)
