from configparser import ConfigParser
import os

configFileName = 'gearshift.ini'
sections = ['clutch', 'shifter', 'miscellaneous']
clutchValues = {
  'controller' : 'Not yet selected',
  'axis'       : '0',
  'reversed'   : '0',
  'bite point' : '90'
 }
shifterValues = {
  'controller' : 'Not yet selected',
  '1st gear' : '0',
  '2nd gear' : '0',
  '3rd gear' : '0',
  '4th gear' : '0',

  '5th gear' : '0',
  '6th gear' : '0',
  '7th gear' : '0',
  '8th gear' : '0',
  'Reverse'  : '0'
  }
miscValues = {
  'shared memory'   : '1',    # 1: read gears, clutch from rF2 shared memory
  'damage'          : '0',    # 1: damage model active
  'shifter'         : '1',    # 0: paddles/sequential. Different damage model
  'double declutch' : '0',    # 1: double declutch required (damage will be worse if not done)  TBD
  'preselector'     : '0',    # 1: pre-selector gearbox TBD
  'reshift'         : '0',    # 1: must go to neutral after a bad shift
  'neutral button'  : 'DIK_NUMPAD0',  # the key code sent to prevent a shift occurring
  'ignition button' : 'DIK_APOSTROPHE', # the key code sent if the engine is damaged
  'wav file'        : 'Grind_default.wav',
  'debug'           : '0',
  'mock input'      : '0',
  'test mode'       : '0',
  'controller_file' : '%ProgramFiles(x86)%/Steam/steamapps/common/rFactor 2/Userdata/player/controller.json'
}


class Config:
  """ docstring """
  def __init__(self):
    # instantiate
    self.config = ConfigParser(interpolation=None)

    # set default values
    for val, default in clutchValues.items():
        self.set('clutch', val, default)
    for val, default in shifterValues.items():
        self.set('shifter', val, default)
    for val, default in miscValues.items():
        self.set('miscellaneous', val, default)

    # if there is an existing file parse values over those
    if os.path.exists(configFileName):
      self.config.read(configFileName)
    else:
      self.write()
      self.config.read(configFileName)

    if self.get('miscellaneous', 'shared memory'):
      self.set('miscellaneous', 'reshift', '0')

  def set(self, section, val, value):
    # update existing value
    if not self.config.has_section(section):
      self.config.add_section(section)
    self.config.set(section, val, value)

  def get(self, section, val):
    try:
      # get existing value
      if val in ['controller', 'wav file', 'neutral button', 'ignition button'] :
        return self.config.get(section, val)
      else:
        return self.config.getint(section, val)
    except: # No such section in file
      self.set(section, val, '')
      return None
  def get_controller_file(self):
      # Special case - expand the path
      return os.path.normpath(
          os.path.expandvars(
              self.config.get('miscellaneous', 'controller_file')))
  def write(self):
    # save to a file
    with open(configFileName, 'w') as configfile:
        self.config.write(configfile)

if __name__ == "__main__":
    # Test
  _config_o = Config()
  section = 'clutch'
  val = 'controller'
  value = _config_o.get(section, val)
  if value:
    if val == 'controller':
      print('%s/%s: %s' % (section, val, value))
    else:
      print('%s/%s: %d' % (section, val, value))
  else:
    print('%s/%s: <None>' % (section, val))
  _config_o.write()
