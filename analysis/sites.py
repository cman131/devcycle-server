from django.contrib.admin.sites import AdminSite

class TourTrakAdmin(AdminSite):
    index_template = '404.html'
    login_template = 'login.html'
    logout_template = 'logout.html'

tt_admin = TourTrakAdmin()

import tour_config.admin
