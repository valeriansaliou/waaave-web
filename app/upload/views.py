import json

from django.http import HttpResponse

from _commons.decorators.security import auth_required
from .forms import UploaderForm
from .models import Upload


@auth_required
def uploader(request):
    response_data = {}

    if request.is_ajax():
        form = UploaderForm(request.POST, request.FILES)
        
        if form.is_valid():
            upload = Upload(
                user=request.user,
                upload=request.FILES['upload'],
            )
            upload.save()

            response_data['status'] = "success"
            response_data['result'] = "Your file has been uploaded:"
            response_data['fileLink'] = "/%s" % upload.upload

            return HttpResponse(json.dumps(response_data), content_type="application/json")

    response_data['status'] = "error"
    response_data['result'] = "We're sorry, but something went wrong. Please be sure that your file respects the upload conditions."

    return HttpResponse(json.dumps(response_data), content_type='application/json')
