import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.forms import model_to_dict
from timeline.models import TimelinePost, TimelineComment
from jsonschema import validate
import jsonschema
from django.core.exceptions import ObjectDoesNotExist, ValidationError

post_schema = {
    'properties': {
        'restaurant_id': {'type': 'string'},
        'user_id': {'type': 'string'},
        'content': {'type': 'string'}
    }
}

comment_schema = {
    'properties': {
        'post_id': {'type': 'string'},
        'user_id': {'type': 'string'},
        'content': {'type': 'string'}
    }
}


def upload_post_page(request):
    """Upload post into post timeline post table"""

    body = json.loads(request.body)
    try:  # validate request
        validate(instance=body, schema=post_schema)
    except jsonschema.exceptions.ValidationError:
        return HttpResponseBadRequest('Invalid request')
    post = TimelinePost(**body)
    post.full_clean()
    post.save()
    post._id = str(post._id)
    return JsonResponse(model_to_dict(post))


def get_all_posts_page(request):
    """ retrieve list of restaurants from database """
    return JsonResponse(TimelinePost.get_all())


def upload_comment_page(request):
    """Upload post into post timeline post table"""

    body = json.loads(request.body)

    try:  # validate request
        validate(instance=body, schema=comment_schema)
    except jsonschema.exceptions.ValidationError:
        return HttpResponseBadRequest('Invalid request')

    try:  # validate post
        post = TimelinePost.objects.get(_id=body['post_id'])
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('Invalid User')

    # create comment
    comment = TimelineComment(**body)
    comment.full_clean()
    comment.save()
    # update post
    post.comments.append(comment._id)
    post.save()

    comment._id = str(comment._id)
    return JsonResponse(model_to_dict(comment))


def get_comment_data_page(request):
    """ Retrieve comment data of given comment from database """
    comment = TimelineComment.objects.get(_id=request.GET.get('_id'))
    comment._id = str(comment._id)
    comment.likes = list(map(str, comment.likes))
    return JsonResponse({'_id': comment._id, 'post_id': comment.post_id, 'user_id': comment.user_id,
                         'likes': comment.likes, 'content': comment.content, 'Timestamp': comment.Timestamp})
