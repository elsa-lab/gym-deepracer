import os


current_dir = os.path.dirname(os.path.realpath(__file__))



ENV_VERSION = {
          0: {'executable_path': os.path.join(current_dir, 'executable/v0/new_york_city.x86_64'),
              'download_id': '1T6Dbuk3A7SVpz2rNFKy4vgbZNFGhPJIL',
              'filename': os.path.join(current_dir, 'executable/v0.zip')},
 
          #1: {'executable_path': os.path.join(current_dir, 'executable/v1/new_york_city.x86_64'),
          #    'download_id': '1Qo1t6fraKSxjyuOw-oTmX2xesN6m_8ir',
          #    'filename': os.path.join(current_dir, 'executable/v1.zip')}
}
