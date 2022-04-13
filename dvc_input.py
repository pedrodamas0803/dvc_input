#!/usr/bin/env python3
# coding: utf-8


from dataclasses import dataclass
import h5py
import os
       
@dataclass
class DVC_Parameters:

    """
    This class will generate an data object containing the parameters for DVC. The default values are:

    INPUTS

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
    image_size:list = []

    OUTPUT

    Data object with DVC parameters.

    """

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

        # checks if the extension provided for the reference image is RAW and argues about the shape of the image
        if self.reference_image.split('.')[-1] == 'raw':
            if image_size == []:
                print(Warning('You will need the size of the raw images to run DVC!!'))
            
            self.image_size = image_size

    def __str__(self):

        """
        This dunder method changes the behavior of the output for the class when 'print(DVC_Parameters)' is called.

        Returns:
            _type_: _description_
        """
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

    """
    This class will generate the model data object. The default values are:

    INPUTS
    basis:str = 'fem',
    nscale:int = 3,
    mesh_size:list = (16, 16, 16))

    """
    def __init__(self,
                basis:str = 'fem',
                nscale:int = 3,
                mesh_size:list = [16, 16, 16]):

        self.basis = basis
        self.nscale = nscale
        self.mesh_size = mesh_size

    def __str__(self):
    
        """
            This dunder method changes the behavior of the output for the class when 'print(DVC_Parameters)' is called.

        """

        string = ("----------------MODEL----------------- \n"+
                 f'Basis function: {self.basis} \n' +
                 f'Coarse graining scales: {self.nscale} \n' +
                 f'Mesh size: {self.mesh_size} \n \n')
        return string

class DVC_H5_Writer(DVC_Parameters, DVC_Model):

    """
    This subclass will inherit from DVC_Parameters and DVC_Model data classes and will configure the exporting of the H5 file.

    If the previously created parameters and model objects are not passed as inputs, the class will create the objects automatically with the default values of each of the classes.

    INPUTS

    parameters:DVC_Parameters = DVC_Parameters(),
    model:DVC_Model = DVC_Model(),
    h5filename:str = './DVC_Settings.h5'


    """
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

        """
        
        Checks if h5 file already exists and ask for confirmation on the decision of overwriting it, otherwise it will just write it. 

        """

        if os.path.exists(self.filename):

            answer = input('There is a file with the name you asked for. Do you want to overwrite it? (y/n)').lower()
            
            if answer == 'y':

                self._fill_h5file()
                print('I wrote the file!')

        else:

            self._fill_h5file()
            print('I wrote the file!')
    
    
    
    def _fill_h5file(self):

        """
        Fills the h5 file with the data.
        """
    
        with h5py.File(name=self.filename, mode='w') as h5file:
            h5file.create_group(name='/param')
            h5file.create_group(name='/model')

            # write the parameters
            h5file.create_dataset(name='/param/analysis', data=self.analysis)
            h5file.create_dataset(name='/param/reference_image', data=self.reference_image)
            h5file.create_dataset(name='/param/deformed_image', data=self.deformed_image)
            h5file.create_dataset(name='/param/result_file', data=self.result_file)
            h5file.create_dataset(name='/param/roi', data=self.roi)
            h5file.create_dataset(name='/param/pixel_size', data=self.pixel_size)
            h5file.create_dataset(name='/param/restart', data=self.restart)
            h5file.create_dataset(name='/param/conv_lim', data=self.conv_lim)
            h5file.create_dataset(name='/param/iter_max', data=self.iter_max)
            h5file.create_dataset(name='/param/regularization_param', data=self.regularization_param)
            h5file.create_dataset(name='/param/regularization_type', data=self.regularization_type)
            h5file.create_dataset(name='/param/psample', data=self.psample)

            # write the model datasets
            h5file.create_dataset(name='/model/basis', data=self.basis)
            h5file.create_dataset(name='/model/nscale', data=self.nscale)
            h5file.create_dataset(name='/model/mesh_size', data=self.mesh_size)

    

