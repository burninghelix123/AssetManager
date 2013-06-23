from distutils.core import setup
setup(name='AssetManager',
      version='1.0',
      description='Dynamic network based asset manager',
      author='Craig Barnett',
      author_email='admin@bhvfx.com',
      url='www.bhvfx.com',
      scripts=['AssetManager/AssetManager.py',],
      packages=['AssetManager.ui', 'AssetManager.functions', 'AssetManager'],)
