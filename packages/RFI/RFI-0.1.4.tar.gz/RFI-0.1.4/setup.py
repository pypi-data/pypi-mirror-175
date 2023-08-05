
from distutils.core import setup
setup(
  name = 'RFI',      
  packages = ['RFI'],  
  version = '0.1.4',     
  license='MIT',       
  description = 'Feature selections methods for classification and regression',  
  author = 'Alejandro Santos and Aitor Hernandez',      
  author_email = 'aitor.hernanadez.1a@gmail.com',     
  url = 'https://github.com/AitorHernandez1/RFI',  
  download_url = 'https://github.com/AitorHernandez1/RFI/archive/refs/tags/RFI_0.1.tar.gz',   
  keywords = ['feature', 'regression', 'classification'],  
  install_requires=[           
          'pandas',
          'sklearn',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',    
    'Intended Audience :: Developers',    
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)




