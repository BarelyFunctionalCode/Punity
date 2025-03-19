import time
import platform

if platform.system() == 'Windows':
  from .windows import get_applications
else:
  from .macos import get_applications

class ExternalApplication:
  def __init__(self, title, size, position):
    self.title = title
    self.position = position
    self.size = size
    self.last_update = time.time()

# Gets the most recent list of applications and updates the applications dictionary
def update_applications(applications):
  current_applications = get_applications()
  for app in current_applications:
    if app['title'] not in applications:
      # Create the application if it doesn't exist
      applications[app['title']] = ExternalApplication(app['title'], app['size'], app['position'])
      print(f'\"{app['title']}\" created at {applications[app['title']].position} with size {applications[app['title']].size}')
    else:
      # Update the application if it does exist
      if app['position'] != applications[app['title']].position or app['size'] != applications[app['title']].size:
        applications[app['title']].last_update = time.time()
        print(f'\"{app['title']}\" moved to {app['position']} with size {app['size']}')

      applications[app['title']].position = app['position']
      applications[app['title']].size = app['size']

  # Delete applications that are no longer open
  application_titles = [app['title'] for app in current_applications]
  delete_keys = []
  for app in applications.keys():
    if app not in application_titles:
      delete_keys.append(app)
  for key in delete_keys:
    del applications[key]