from rest_framework import routers
from bpmn.views import diagram_view

router = routers.DefaultRouter()
router.register(r'diagrams', diagram_view.DiagramViewset)