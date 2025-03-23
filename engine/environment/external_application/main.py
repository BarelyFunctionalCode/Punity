import time
import platform

if platform.system() == 'Windows':
  from .windows import get_applications
else:
  from .macos import get_applications


class ExternalApplication:
  def __init__(self, pid, name, title, size, position):
    self.pid = pid
    self.name = name
    self.title = title
    self.position = position
    self.size = size
    self.last_update = time.time()

# Gets the most recent list of applications and updates the applications dictionary
def update_applications(applications):
  current_applications = get_applications()
  for app in current_applications:
    if app['pid'] not in applications:
      # Create the application if it doesn't exist
      applications[app['pid']] = ExternalApplication(**app)
      # print(f'\"{app['name']}\" created at {applications[app['pid']].position} with size {applications[app['pid']].size} and pid {applications[app['pid']].pid} ({applications[app['pid']].title})')
    else:
      # Update the application if it does exist
      if app['position'] != applications[app['pid']].position or app['size'] != applications[app['pid']].size or app['title'] != applications[app['pid']].title:
        applications[app['pid']].last_update = time.time()
        # print(f'\"{app['name']}\" moved to {app['position']} with size {app['size']} ({app['title']})')

      applications[app['pid']].position = app['position']
      applications[app['pid']].size = app['size']
      applications[app['pid']].title = app['title']

  # Delete applications that are no longer open
  application_titles = [app['pid'] for app in current_applications]
  delete_keys = []
  for app in applications.keys():
    if app not in application_titles:
      delete_keys.append(app)
  for key in delete_keys:
    del applications[key]